import os, logging, traceback, datetime
from struct import unpack, pack
import numpy as np
from aug_sfutils import sfmap, sfobj, manage_ed, parse_kwargs, str_byt, libddc, getlastshot
from aug_sfutils.sfmap import ObjectID as oid

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')

logger = logging.getLogger('aug_sfutils')

if len(logger.handlers) == 0:
    hnd = logging.StreamHandler()
    hnd.setFormatter(fmt)
    logger.addHandler(hnd)

logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

n_rel = 8
SFHbuflen = 128000
PPGCLOCK  = [1e-6, 1e-5, 1e-4, 1e-3]
LOGICAL   = sfmap.typeMap('descr', 'SFfmt', 'LOGICAL')
LONGLONG  = sfmap.typeMap('descr', 'SFfmt', 'LONGLONG')


def read_other_sf(*args, **kwargs):

    return SFREAD(*args, **kwargs)


def getChunk(fname, start, length):
    """Reads the requested byteblock from the binary shotfile"""
    rdata = None
    with open(fname, 'rb') as f:
        f.seek(start)
        rdata = f.read(length)
    return rdata


def getcti_ts06(nshot):
    """Gets the absolute time (ns) of a discharge trigger"""

    diag = 'CTI'
    cti = SFREAD(nshot, diag)
    try:
        cdev = cti.LAM.data
        ts06 = cdev['PhyReset']
        if ts06 == 0:
            ts06 = cdev['TS06']
        if ts06 == 0:
            ts06 = cdev['CT_TS06']
    except: # shot < 35318
        cdev = cti.TS6.data
        ts06 = cdev['TRIGGER']
        logger.debug('getcti_ts06 %d', ts06)
    if ts06 < 1e15:
        ts06 = None
    return ts06


def ppg_time(tbobj): # Bug MAG:27204
    """Returns the time-array in [s] for TB of type PPG_prog"""

    for robj in tbobj.relobjects:
        if robj.objectType == oid.Device:
            ppg = robj.data # Device/ParSet dictionary
            npt = tbobj.n_pre
            nsteps = tbobj.n_steps
            if not 'PRETRIG' in ppg.keys():
                continue
            if npt > 0:
                if ppg['PRETRIG'] > 0:
                    dt = ppg['RESOLUT'][15] * PPGCLOCK[ppg['RESFACT'][15]] + 1e-6
                else:
                    dt = 0.
                start_time = -dt*npt #ppg['PULSES'][0]
            else:
                start_time = 0.
            nptyp = sfmap('SFfmt', 'np', tbobj.data_format)
            start_phase = start_time
            if npt > 0:
                time_ppg = dt*np.arange(npt, dtype=nptyp) + start_phase
                start_phase = time_ppg[-1] + dt
            else:
                time_ppg = []
            for jphase in range(16):
                if ppg['PULSES'][jphase] > 0:
                    dt = ppg['RESOLUT'][jphase]*PPGCLOCK[ppg['RESFACT'][jphase]]
                    tb_phase = dt*np.arange(ppg['PULSES'][jphase], dtype=nptyp) + start_phase
                    time_ppg = np.append(time_ppg, tb_phase)
                    start_phase = time_ppg[-1] + dt
                    logger.debug('Start time %d %d %d %d %.4f %.4f', jphase, ppg['PULSES'][jphase], ppg['RESOLUT'][jphase], ppg['RESFACT'][jphase], dt, start_phase)
            if len(time_ppg) == 0:
                return None
            else:
                return time_ppg[:nsteps]
    return None


class SFREAD(dict):


    def __init__(self, *args, **kwargs):

        self.__dict__ = self

        self.properties = type('', (), {})()
        self.properties.shot   = None
        self.properties.diag   = None
        self.properties.exp    = None
        self.properties.status = False
        self.open(*args, **kwargs)
        if len(args) > 2:
            logger.warning('More than 2 explicit arguments: only the first two (diag, shot) are retained')


    def open(self, *args, **kwargs):

        if 'sfh' in kwargs.keys():
            self.properties.path = kwargs['sfh']
            self.properties.shot = 0
            self.properties.ed = 0
            self.properties.diag = os.path.basename(self.properties.path)[:3]

        elif 'sf' in kwargs.keys():
            self.properties.path = os.path.abspath(kwargs['sf'])
            dirs = self.properties.path.split('/')[::-1]
            sshot = ''
            for subdir in dirs:
                try:
                    a = float(subdir)
                    sshot = subdir + sshot
                except:
                    self.properties.diag = subdir
                    break
            self.properties.shot = int(sshot.split('.')[0])

        else:

            n_args = len(args)
            if n_args == 0:
                logger.warning('No argument given, need at least diag_name')
                return
            if isinstance(args[0], str) and len(args[0].strip()) == 3:
                diag = args[0].strip()
                if n_args > 1:
                    if isinstance(args[1], (int, np.integer)):
                        nshot = args[1]
            elif isinstance(args[0], (int, np.integer)):
                nshot = args[0]
                if n_args > 1:
                    if isinstance(args[1], str) and len(args[1].strip()) == 3:
                        diag = args[1].strip()
            if 'nshot' not in locals():
                logger.warning('No argument is a shot number (int), taking last AUG shot')
                nshot = getlastshot.getlastshot()
            if 'diag' not in locals():
                diag = input('Please enter a diag_name (str(3), no delimiter):\n')

            exp = parse_kwargs.parse_kw( ('exp', 'experiment'), kwargs, default='AUGD')
            ed  = parse_kwargs.parse_kw( ('ed', 'edition'), kwargs, default=0)
            logger.debug('%d %s %s %d', nshot, diag, exp, ed)
            self.properties.path, self.properties.ed = manage_ed.sf_path(nshot, diag, exp=exp, ed=ed)
            if self.properties.path is None:
                logger.error('Shotfile not found for %s:%s(%d) #%d', exp, diag, ed, nshot)
                return
            else:
                self.properties.shot = nshot
                self.properties.diag = diag.upper()
                self.properties.exp  = exp  # unused herein, but useful docu

# Parse shotfile header including content of ParamSets and Devices

        self.read_sfh()
        self.set_relations()

        if hasattr(self, 'addrlen'):
            size_fac = sfmap.addrsizes[self.addrlen]
            for obj in self.properties.objects:
                self.__dict__[obj].address *= size_fac

        self.properties.cache = {}
        self.properties.time = datetime.datetime.fromtimestamp(os.path.getctime(self.properties.path))


    def __call__(self, name):

        if not self.properties.status:
            return None

        if name in self.properties.parsets:
            return self.__dict__[name].pars

        if name not in self.properties.cache.keys():
            if name in self.properties.objects:
                self.properties.cache[name] = self.getobject(name)
            elif name not in self.properties.parsets:
                logger.error('Signal %s:%s not found for shot #%d', self.properties.diag, name, self.properties.shot)
                return None
        return self.properties.cache[name]


    def read_sfh(self):

        """Reads a full shotfile header, including the content of ParamSets and Devices"""

        sfile = self.properties.path
        logger.info('Fetching SF %s', sfile)
        if not os.path.isfile(sfile):
            logger.error('Shotfile %s not found' %sfile)
            return

        self.properties.lists   = []
        self.properties.parsets = []
        self.properties.objects = []
# Read first 128kB of binary shotfile
        byt_str = getChunk(self.properties.path, 0, SFHbuflen)
        if len(byt_str) < 128:
            logger.error('Error: shotfile %s has < 128 bytes, ignored' %(sfile))
            self.properties.status = None
            return
        self.properties.byt_str = byt_str

        n_max = 1000
        n_obj = n_max
        self.properties.related = []
        for j in range(n_max):
            sfo = SF_OBJECT(j, self.properties)
            if hasattr(sfo, 'objectType'):
                sfo.objid = j
                onam = str_byt.to_str(sfo.objectName.strip())
                if sfo.objectType == oid.Diagnostic:
                    if n_obj == n_max: # There might be several diags objects in a SFH
                        n_obj = sfo.num_objs
                self.properties.related.append(onam)
                if sfo.objectType in (oid.ParamSet, oid.Device):
                    self.properties.parsets.append(onam)
                    sfo.getData()
                elif sfo.objectType == oid.List:
                    self.properties.lists.append(onam)
                    sfo.getData()
                elif sfo.objectType in (oid.SignalGroup, oid.Signal, oid.TimeBase, oid.AreaBase):
                    self.properties.objects.append(onam)
                self.__dict__[onam] = sfo
            if j >= n_obj - 1:
                break


    def set_relations(self):

        for key, sfo in self.__dict__.items():
            if key not in ('properties', 'cache'):
                sfo.relations  = [self.properties.related[jid] for jid in sfo.rel if jid != 65535]
                sfo.relobjects = [self.__dict__[self.properties.related[jid]] for jid in sfo.rel if jid != 65535]
                if sfo.objectType == oid.List:
                    sfo.data = [self.properties.related[jid] for jid in sfo.data]
                elif sfo.objectType == oid.Device:
                    if 'TS06' in sfo.data.keys(): # former get_ts06
                        ts06 = sfo.data['TS06']
                        if ts06 > 1e15:
                            sfo.ts06 = ts06
                elif sfo.objectType in (oid.Signal, oid.SignalGroup):
                    for robj in sfo.relobjects:
# check where the timebase relation is
                        if robj.objectType == oid.TimeBase:
                            shape_arr = sfo.index[::-1][:sfo.num_dims]
                            nt = robj.n_steps
                            if shape_arr.count(nt) == 1:
                                sfo.time_dim = shape_arr.index(nt)
                            sfo.timebase = robj.objectName
# For data calibration
                            if sfo.phys_unit == 'counts':
                                sfo.cal_fac = robj.s_rate
                        elif robj.objectType == oid.AreaBase:
                            sfo.areabase = robj.objectName
# Calibration parameters
                        elif robj.objectType  == oid.ParamSet:
                            if robj.cal_type == sfmap.CalibType.LinCalib:
                                sfo.calib_pars = robj.data
                            elif robj.cal_type == extCalib:
                                diag_ext = robj.data['DIAGNAME']
                                diag_ext = ''.join([str_byt.to_str(x) for x in diag_ext])
                                shot_ext = libddc.previousshot(diag_ext, shot=self.properties.shot)
                                ext = read_other_sf(shot_ext, diag_ext) # ParSet same name in external shotfile
                                sfo.calib_pars = ext.__dict__[robj.objectName].data


class SF_OBJECT:
    """Reads a generic object's metadata from the SFH's 128byte string"""


    def __init__(self, jobj, properties):

        self.properties = properties
        self.sfname = self.properties.path
        sfh_byte_str = getChunk(self.sfname, 0, SFHbuflen)
        if len(sfh_byte_str) < 128:
            logger.error('Error: shotfile %s has < 128 bytes, ignored', self.sfname)
            return

        byte_str = sfh_byte_str[jobj*128: (jobj+1)*128]
        self.objectName = str_byt.to_str(byte_str[0:8])

        if not self.objectName:
            logger.error('Error: empty object name')
            return

        self.objectType, self.level, self.status = unpack('>3H', byte_str[ 8: 14])
        typ = self.objectType

        self.object_type = 'Unknown'
        for key, val in sfmap.ObjectID.__dict__.items():
            if typ == val:
                self.object_type = key
                break
        self.errcode  = unpack('>h', byte_str[14: 16])[0]
        fmt = '>%dH' %n_rel
        self.rel      = list(unpack(fmt,  byte_str[16        : 16+2*n_rel]))
        self.address, self.length = unpack('>2I', byte_str[16+2*n_rel: 24+2*n_rel])
        val = byte_str[40:  64]
        logger.debug(self.objectName)
        self.descr    = str_byt.to_str(byte_str[64: 128].strip())
        logger.debug(self.descr)

        if typ == oid.Diagnostic:
            self.diag_code = val[: 4]
            self.num_objs, self.diag_type  = unpack('>2H', val[4: 8])
            self.shot_nr , self.c_time     = unpack('>2I', val[8: 16])
            self.up_limit, self.exp, self.version, self.s_type = unpack('>4H', val[16: 24])

        elif typ == oid.List:
            self.data_format, self.nitems, self.ordering, self.list_type = unpack('>4H', val[ : 8])

        elif typ == oid.Device:
            self.data_format, self.acquseq, self.nitems, self.dev_type = unpack('>4H', val[:8])
            self.dev_addr, self.n_chan  = unpack('>2I', val[ 8: 16])
            self.task    , self.dev_num = unpack('>2H', val[16: 20])
            self.n_steps                = unpack('>I' , val[20: 24])[0]

        elif typ == oid.ParamSet:
            self.nitems, self.cal_type = unpack('>2H', val[4: 8])
            for key, val in sfmap.CalibType.__dict__.items():
                if self.cal_type == val:
                    self.calibration_type = key
                    break

        elif typ == oid.MapFunc:
            self.nitems, self.map_type = unpack('>2H' , val[4: 8])
            self.task = unpack('>H' , val[16: 18])[0]

        elif typ in (oid.SignalGroup, oid.Signal):
            self.data_format, self.physunit, self.num_dims = unpack('>3H' , val[: 6])
            if self.physunit in sfmap.unit_d.keys():
                self.phys_unit = sfmap.unit_d[self.physunit]
            else:
                logger.warning('No phys. unit found for object %s, key=%d', self.objectName, self.physunit)
                self.phys_unit = ''
            self.stat_ext = unpack('>h' , val[6: 8])[0]
            self.index    = list(unpack('>4I', val[8: 24]))

        elif typ == oid.TimeBase:
            self.data_format, self.burstcount, self.event, self.tbase_type = unpack('>4H', val[: 8])
            self.s_rate = unpack('>I', val[ 8: 12])[0] #Hz
            self.n_pre, self.n_steps = unpack('>2I', val[16: 24])
            for key, val in sfmap.TimebaseType.__dict__.items():
                if self.tbase_type == val:
                    self.timebase_type = key
                    break

        elif typ == oid.SFList:
            self.nitems = unpack('>H', val[2: 4])

        elif typ == oid.Algorithm:
            self.hostname = val[ 8: 16]
            self.date     = val[16: 24]

        elif typ == oid.UpdateSet:
            self.nitems =  unpack('>H' , val[ 2: 4])[0]
            self.input_vals = unpack('>i' , val[ 4: 8])[0]
            self.next_index, self.size = unpack('>I' , val[ 16: 24])

        elif typ == oid.LocTimer:
            self.data_format, self.resolution = unpack('>2H', val[: 4])
            self.size = unpack('>I', val[20: 24])[0]

        elif typ == oid.AreaBase:
            self.data_format = unpack('>H' , val[ : 2])[0]
            self.physunit    = unpack('>3H', val[2: 8])
            self.phys_unit = [sfmap.unit_d[x] for x in self.physunit]
            self.size_x, self.size_y, self.size_z, self.n_steps = unpack('>4I' , val[8: 24])
            self.sizes = [self.size_x, self.size_y, self.size_z]

        elif typ == oid.Qualifier:
            self.data_format = unpack('>H' , val[ : 2])[0]
            self.num_dims, self.qsub_typ = unpack('>2H' , val[4: 8])
            self.index_4, self.index_3, self.index_2, self.max_sections = unpack('>4I' , val[8: 24])

        elif typ == oid.ModObj:
            self.nitems = unpack('>H' , val[ : 2])[0]

        elif typ == oid.MapExtd:
            self.nitems, self.mapalg = unpack('>2H', val[ :  4])
            self.tbeg  , self.tend   = unpack('>2I', val[4: 12])
            val_0, val_1  = unpack('>2H', val[12: 16])
            val_2, val_3  = unpack('>2I', val[16: 24])

        elif typ == oid.Resource:
            self.num_cpus, self.first_cpu = unpack('>2H' , val[ : 4])

        elif typ == oid.ADDRLEN:
            self.addrlen = unpack('>H' , val[ : 2])[0]


    def getData(self, cal=True, tbeg=None, tend=None):

        if self.objectType in (oid.ParamSet, oid.Device):
            self.getParamSet()
        elif self.objectType == oid.List:
            self.getList()
        elif self.objectType in (oid.TimeBase, oid.AreaBase, oid.Signal, oid.SignalGroup):
            self.getObject(cal=cal, tbeg=None, tend=None)


    def getList(self):

        buf = getChunk(self.sfname, self.address, self.length)
        sfmt = sfmap.typeMap('SFfmt', 'struc', self.data_format)
        self.data = unpack('>%d%s' %(self.nitems, sfmt), buf) # IDs, not labels

        
    def getParamSet(self):
        """Returns data and metadata of a Parameter Set.
        Called by default on SFH reading"""

        buf = getChunk(self.sfname, self.address, self.length)

        j0 = 0
        self.data = {}
        logger.debug('PS: %s, addr: %d, length: %d', self.objectName, self.nitems, self.length)
        for j in range(self.nitems):
            pname = str_byt.to_str(buf[j0: j0+8])
            unit, dfmt, n_items = unpack('>3h', buf[j0+8:  j0+14])
            meta = type('', (), {})()
            meta.physunit = unit
            if unit in sfmap.unit_d.keys():
                meta.phys_unit = sfmap.unit_d[unit]
            meta.n_items = n_items
            meta.data_format = dfmt
            meta.status = unpack('>h', buf[j0+14:  j0+16])[0]
            logger.debug('PN: %s, j0: %d, unit: %d dfmt: %d n_items: %d, status: %d', pname, j0, unit, dfmt, n_items, meta.status)
            j0 += 16

            if dfmt in sfmap.fmt2len.keys(): # char variable
                dlen = sfmap.fmt2len[dfmt]
                bytlen = n_items * dlen
                meta.dmin = buf[j0  : j0+1]
                meta.dmax = buf[j0+1: j0+2]
                if len(meta.dmin) == 0:
                    meta.dmin = b' '
                if len(meta.dmax) == 0:
                    meta.dmax = b' '
                data = np.chararray((n_items,), itemsize=dlen, buffer=buf[j0+2: j0+2+bytlen])
                dj0 = 8 * ( (bytlen + 9)//8 )
                j0 += dj0
            elif dfmt in sfmap.dataTypes['SFfmt']:
                sfmt = sfmap.typeMap('SFfmt', 'struc', dfmt)
                logger.debug('Numerical par %d', dfmt)
                val_len = n_items + 2
                bytlen = val_len * np.dtype(sfmt).itemsize
                if dfmt == sfmap.typeMap('descr', 'SFfmt', 'LOGICAL'): # Logical, bug if n_items > 1?
                    meta.dmin = unpack(sfmt, buf[j0  : j0+1])[0]
                    meta.dmax = unpack(sfmt, buf[j0+3: j0+4])[0]
                    data = unpack(sfmt, buf[j0+5: j0+6])[0]
                else:
                    data = np.ndarray((val_len, ), '>%s' %sfmt, buf[j0: j0+bytlen], order='F').copy()
                    meta.dmin = data[0]
                    meta.dmax = data[1]
                    data = np.squeeze(data[2:]) # no array if n_items=1
                dj0 = str_byt.next8(bytlen)
                j0 += dj0
            else: # faulty dfmt
                break
            self.data[pname] = sfobj.SFOBJ(data, sfho=meta)

            if j0 >= self.length:
                break


    def getObject(self, cal=True, nbeg=None, nend=None, tbeg=None, tend=None):

        otyp = self.objectType

        if otyp in (oid.SignalGroup, oid.Signal):
            shape_arr = np.array(self.index[::-1][:self.num_dims])
        elif otyp == oid.TimeBase:
            shape_arr = np.array([self.n_steps])
        elif otyp == oid.AreaBase:
            shape_arr = np.array([self.size_x + self.size_y + self.size_z, self.n_steps])
            logger.debug('%d %d', *shape_arr)
        else:
            logger.error('Object %s is no signal, signalgroup, timebase nor areabase, skipping')
            return None

        dfmt = self.data_format
        logger.debug('TB %s %d %d %d', self.objectName, otyp, self.length, dfmt)
        if otyp == oid.TimeBase and self.length == 0:
            if self.tbase_type == sfmap.TimebaseType.PPG_prog: # e.g. END:T-LM_END
                self.data = ppg_time(obj)
            else:   # ADC_intern, e.g. DCN:T-ADC-SL
                self.data = (np.arange(self.n_steps, dtype=np.float32) - self.n_pre)/self.s_rate
        else:
            if dfmt in sfmap.fmt2len.keys(): # char variable
                dlen = sfmap.fmt2len[dfmt]
                bytlen = np.prod(shape_arr) * dlen
                self.data = np.chararray(shape_arr, itemsize=dlen, buffer=getChunk(self.sfname, self.address, bytlen), order='F')
            else: # numerical variable
                sfmt = sfmap.typeMap('SFfmt', 'struc', dfmt)
                type_len = np.dtype(sfmt).itemsize
                addr = self.address
                bytlen = np.prod(shape_arr) * type_len
                if otyp in (oid.Signal, oid.TimeBase, oid.AreaBase) or self.time_last():
                    if nbeg is None:
                        nbeg = 0
                    else:
                        byt_beg = nbeg*np.prod(shape_arr[:-1])
                        addr   += byt_beg*type_len
                        bytlen -= byt_beg*type_len
                        shape_arr[-1] -= nbeg
                    if nend is not None:
                        bytlen = (nend - nbeg)*np.prod(shape_arr[:-1])*type_len
                        shape_arr[-1] = nend - nbeg

                self.data = np.ndarray(shape_arr, '>%s' %sfmt, getChunk(self.sfname, addr, bytlen), order='F')

# LongLong in [ns] and no zero at TS06
            if otyp == oid.TimeBase and dfmt == LONGLONG and cal: # RMC:TIME-AD0, SXS:Time
                logger.debug('Before getts06 dfmt:%d addr:%d len:%d data1:%d, %d', dfmt, addr, bytlen, data[0], data[1])
                self.data = 1e-9*(self.data - self.getts06())
                logger.debug('%d',  self.getts06())

            self.calib = False
# Calibrated signals and signal groups
            if otyp in (oid.SignalGroup, oid.Signal):
                if cal:
                    self.raw2calib()


    def raw2calib(self):
        """Calibrates an uncalibrated signal or SignalGroup"""

# Calibrated signals and signal groups
        if self.objectType not in (oid.SignalGroup, oid.Signal):
            logging.error('Calibration failed for %s: no Sig, no SGR', obj)
            return #self.data unchanged

        if not hasattr(self, 'calib_pars'):
            if hasattr(self, 'cal_fac'):
                self.data = self.cal_fac*np.float32(self.data)
            return

        for j in range(10):
            mult = 'MULTIA0%d' %j
            shif = 'SHIFTB0%d' %j
            if mult in pscal.keys():
# we need to fix the content of pscal for signagroups
# assuming first entry wins
                if j == 0:
                    dout = self.data*1. # Creates a copy of a read-only array, only once
                    dout.calib = True
                multi = np.atleast_1d(pscal[mult])
                shift = np.atleast_1d(pscal[shif])
                if self.objectType == oid.Signal or len(multi) == 1:
                    dout *= multi[0] # MXR
                    dout += shift[0]
                else:
                    n_pars = dout.shape[1]
                    if n_pars != len(multi):
                        logger.warning('Inconsitent sizes in calibration PSet %s', obj)
                    if n_pars <= len(multi):
                        dout *= multi[: n_pars] # BLB
                        dout += shift[: n_pars]
                    else:
                        dout *= multi[0]
                        dout += shift[0]
            else:
                break
        if 'dout' in locals():
            self.data = dout


    def getts06(self):
        """
        Reads the diagnostic internal TS06 from parameter set
        """
        ts06 = None
        if self.objectType == oid.TimeBase:
            tb = obj
        else:
            for robj in self.relobjects:
                if robj.objectType == oid.TimeBase: # related TB
                    tb = robj
                    break
        if 'tb' in locals(): # No TB related
            obj2 = tb
        else: # try a direct relation
            obj2 = obj

        for robj in obj2.relobjects:
            if robj.objectType == oid.Device: # related device
                if 'TS06' in robj.data.keys():
                    ts6 = robj.data['TS06']
                    if ts6 > 1e15:
                        ts06 = ts6
                        break

        logger.debug('getts06 %s %d', rel_obj, ts06)
        if ts06 is None:
            if hasattr(self, 'ts06'):
                ts06 = self.ts06
            else:
                ts06 = getcti_ts06(self.properties.shot)

        return ts06


    def time_first(self):
        """True if SigGroup has time as first coordinate"""

        if self.objectType != oid.SignalGroup:
            return False

        return (self.time_dim == 0)


    def time_last(self):
        """True if SigGroup has time as last coordinate"""

        if self.objectType != oid.SignalGroup:
            return False

        return (self.time_dim == self.num_dims-1)


if __name__ == '__main__':

    sfile = '/afs/ipp/home/a/augd/shots/2805/L1/CEZ/28053.3'
    nshot = 28053
    diag = 'CEZ'
    cez = SFREAD(diag, nshot)
    print(cez.properties.time)
    print(cez.Ti.phys_unit)
    print(cez.properties.parsets)
    print(cez.LOSInfo.__dict__)
    cez.Ti.getData()
    titim = cez[cez.Ti.timebase]
    titim.getData()
    tiarea = cez[cez.Ti.areabase]
    tiarea.getData()
    print(cez.Ti.data[0, :])
    print(titim.data[:50])
    print(tiarea.data.shape)
    print(cez.Ti.areabase)
    print(cez.Ti.timebase)
    print(cez.SIGNALS.data)
