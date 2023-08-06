import os, logging, traceback
from struct import unpack
import numpy as np
from aug_sfutils import sfmap, sfobj, str_byt
from aug_sfutils.sfmap import ObjectID as oid

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')

logger = logging.getLogger('aug_sfutils.read')

if len(logger.handlers) == 0:
    hnd = logging.StreamHandler()
    hnd.setFormatter(fmt)
    logger.addHandler(hnd)

logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

n_rel = 8
PPGCLOCK = [1e-6, 1e-5, 1e-4, 1e-3]
LOGICAL  = sfmap.typeMap('descr', 'SFfmt', 'LOGICAL')


def getChunk(fname, start, length):
    """Reads the requested byteblock from the binary shotfile"""
    rdata = None
    with open(fname, 'rb') as f:
        f.seek(start)
        rdata = f.read(length)
    return rdata


class SF_READ(dict):


    def __init__(self, sfpath):

        self.__dict__ = self

        if not os.path.isfile(sfpath):
            logger.error('Shotfile %s not found', sfpath)
            return None

        self.properties = type('', (), {})()
        self.properties.path = sfpath

        self.read_sfh()
        self.set_attributes()


    def read_sfh(self, psets=True):
        """Reads a full shotfile header, including the data of ParamSets, Devices, Lists"""

        sfile = self.properties.path

        self.properties.lists   = []
        self.properties.parsets = []
        self.properties.objects = []
        self.properties.SFobjects = []
        self.properties.addrlen = 1

        n_max = 1000
        n_obj = n_max
        self.properties.related = []
        for j in range(n_max):
            sfo = SF_OBJECT(j, self.properties)
            if hasattr(sfo, 'objectType'):
                sfo.objid = j
                onam = str_byt.to_str(sfo.objectName.strip())
                if sfo.objectType == oid.Diagnostic:
                    self.properties.shot = sfo.shot_nr
                    if n_obj == n_max: # There might be several diags objects in a SFH
                        n_obj = sfo.num_objs
                self.properties.related.append(onam)
                self.properties.SFobjects.append(sfo)
                if sfo.objectType in (oid.ParamSet, oid.Device):
                    self.properties.parsets.append(onam)
                elif sfo.objectType == oid.List:
                    self.properties.lists.append(onam)
                elif sfo.objectType in (oid.SignalGroup, oid.Signal, oid.TimeBase, oid.AreaBase):
                    self.properties.objects.append(onam)
                elif sfo.objectType in (oid.ADDRLEN, ):
                    self.properties.addrlen = sfmap.addrsizes[sfo.addrlen]
                self.__dict__[onam] = sfo
            if j >= n_obj - 1:
                break


    def set_attributes(self):
        """Sets useful context info for the entire shotfile"""

        for sfo in self.properties.SFobjects:
            sfo.address *= self.properties.addrlen
            sfo.relations  = [self.properties.related[jid]   for jid in sfo.rel if jid != 65535]
            sfo.relobjects = [self.properties.SFobjects[jid] for jid in sfo.rel if jid != 65535]
            if hasattr(sfo, 'dataFormat'):
                if sfo.dataFormat in sfmap.dataTypes['SFfmt'].values:
                    sfo.dataType = sfmap.typeMap('SFfmt', 'descr', sfo.dataFormat)
            if sfo.objectType == oid.List:
                sfo.getData()
                sfo.data = [self.properties.related[jid] for jid in sfo.data]

            elif sfo.objectType in (oid.Device, oid.ParamSet):
                sfo.getData()
                if sfo.objectType in (oid.Device, ):
                    if 'TS06' in sfo.data.keys(): # former get_ts06
                        ts06 = sfo.data['TS06']
                        if ts06 > 1e15:
                            sfo.ts06 = ts06

            elif sfo.objectType in (oid.Signal, oid.SignalGroup):
                for jrel, robj in enumerate(sfo.relobjects):
# check where the related timebase is
                    if robj.objectType == oid.TimeBase:
                        shape_arr = sfo.index[::-1][:sfo.num_dims]
                        nt = robj.n_steps
                        if shape_arr.count(nt) == 1:
                            sfo.time_dim = shape_arr.index(nt)
                        sfo.timebase = robj
                        sfo.time_dim = jrel
# For data calibration
                        if sfo.phys_unit == 'counts':
                            sfo.cal_fac = robj.s_rate
# check where the related areabase is
                    elif robj.objectType == oid.AreaBase:
                        sfo.areabase = robj
                        sfo.area_dim = jrel


class SF_OBJECT:
    """Reads the metadata of a generic SF object (sfo) from the SFH's 128byte string.
    For data, call getData()"""


    def __init__(self, jobj, properties):

        self.properties = properties
        self.sfname = self.properties.path
        byte_str = getChunk(self.sfname, jobj*128, 128)

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
        self.rel = list(unpack(fmt,  byte_str[16 : 16+2*n_rel]))
        self.address, self.length = unpack('>2I', byte_str[16+2*n_rel: 24+2*n_rel])
        val = byte_str[40:  64]
        logger.debug('%s %d %d', self.objectName, self.address, self.length)
        self.descr    = str_byt.to_str(byte_str[64: 128].strip())
        logger.debug(self.descr)

        if typ == oid.Diagnostic:
            self.diag_code = val[: 4]
            self.num_objs, self.diag_type  = unpack('>2H', val[4: 8])
            self.shot_nr , self.c_time     = unpack('>2I', val[8: 16])
            self.up_limit, self.exp, self.version, self.s_type = unpack('>4H', val[16: 24])

        elif typ == oid.List:
            self.dataFormat, self.nitems, self.ordering, self.list_type = unpack('>4H', val[ : 8])

        elif typ == oid.Device:
            self.dataFormat, self.acquseq, self.nitems, self.dev_type = unpack('>4H', val[:8])
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
            self.dataFormat, self.physunit, self.num_dims = unpack('>3H' , val[: 6])
            if self.physunit in sfmap.unit_d.keys():
                self.phys_unit = sfmap.unit_d[self.physunit]
            else:
                logger.warning('No phys. unit found for object %s, key=%d', self.objectName, self.physunit)
                self.phys_unit = ''
            self.stat_ext = unpack('>h' , val[6: 8])[0]
            self.index    = list(unpack('>4I', val[8: 24]))

        elif typ == oid.TimeBase:
            self.dataFormat, self.burstcount, self.event, self.tbase_type = unpack('>4H', val[: 8])
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
            self.nitems     = unpack('>H', val[ 2: 4])[0]
            self.input_vals = unpack('>i', val[ 4: 8])[0]
            self.next_index, self.size = unpack('>I', val[ 16: 24])

        elif typ == oid.LocTimer:
            self.dataFormat, self.resolution = unpack('>2H', val[: 4])
            self.size = unpack('>I', val[20: 24])[0]

        elif typ == oid.AreaBase:
            self.dataFormat = unpack('>H' , val[ : 2])[0]
            self.physunit   = unpack('>3H', val[2: 8])
            self.phys_unit = [sfmap.unit_d[x] for x in self.physunit]
            self.size_x, self.size_y, self.size_z, self.n_steps = unpack('>4I', val[8: 24])
            self.sizes = [self.size_x, self.size_y, self.size_z]

        elif typ == oid.Qualifier:
            self.dataFormat = unpack('>H', val[ : 2])[0]
            self.num_dims, self.qsub_typ = unpack('>2H', val[4: 8])
            self.index_4, self.index_3, self.index_2, self.max_sections = unpack('>4I', val[8: 24])

        elif typ == oid.ModObj:
            self.nitems = unpack('>H', val[ : 2])[0]

        elif typ == oid.MapExtd:
            self.nitems, self.mapalg = unpack('>2H', val[ :  4])
            self.t_beg , self.t_end  = unpack('>2I', val[4: 12])
            val_0, val_1  = unpack('>2H', val[12: 16])
            val_2, val_3  = unpack('>2I', val[16: 24])

        elif typ == oid.Resource:
            self.num_cpus, self.first_cpu = unpack('>2H', val[ : 4])

        elif typ == oid.ADDRLEN:
            self.addrlen = unpack('>H', val[ : 2])[0]


    def getData(self, nbeg=0, nend=None):
        """Stores the data part of a SF object into sfo.data"""

        if self.objectType in (oid.ParamSet, oid.Device):
            self.getParamSet()
        elif self.objectType == oid.List:
            self.getList()
        elif self.objectType in (oid.TimeBase, oid.AreaBase, oid.Signal, oid.SignalGroup):
            self.getObject(nbeg=nbeg, nend=nend)


    def getList(self):
        """Stores the object IDs contained in a SF list (such as SIGNALS)"""

        buf = getChunk(self.sfname, self.address, self.length)
        sfmt = sfmap.typeMap('SFfmt', 'struc', self.dataFormat)
        self.data = unpack('>%d%s' %(self.nitems, sfmt), buf) # IDs, not labels


    def getParamSet(self):
        """Returns data and metadata of a Parameter Set.
        Called by default on SFH reading"""

        buf = getChunk(self.sfname, self.address, self.length)

        j0 = 0
        self.data = {}
        logger.debug('PS: %s, addr: %d, n_item: %d, length: %d', self.objectName, self.address, self.nitems, self.length)
        for j in range(self.nitems):
            pname = str_byt.to_str(buf[j0: j0+8])
            unit, dfmt, n_items = unpack('>3h', buf[j0+8:  j0+14])
            meta = type('', (), {})()
            meta.physunit = unit
            if unit in sfmap.unit_d.keys():
                meta.phys_unit = sfmap.unit_d[unit]
            meta.n_items = n_items
            meta.dataFormat = dfmt
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
            elif dfmt in sfmap.dataTypes['SFfmt'].values:
                sfmt = sfmap.typeMap('SFfmt', 'struc', dfmt)
                logger.debug('Numerical par %d', dfmt)
                val_len = n_items + 2
                bytlen = val_len * np.dtype(sfmt).itemsize
                if n_items >= 0:
                    if dfmt == LOGICAL: # Logical, bug if n_items > 1?
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


    def getObject(self, nbeg=0, nend=None):
        """Stores data part of Sig, SigGrou, TimeBase, AreaBase"""

        otyp = self.objectType
        if hasattr(self, 'nbeg'):
           if self.nbeg == nbeg and self.nend == nend:
               return # do not re-read object if data are there already
        self.nbeg = nbeg
        self.nend = nend
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

        dfmt = self.dataFormat
        if otyp == oid.TimeBase and self.length == 0:
            if self.tbase_type == sfmap.TimebaseType.PPG_prog: # e.g. END:T-LM_END
                self.ppg_time()
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
                    byt_beg = nbeg*np.prod(shape_arr[:-1])
                    addr   += byt_beg*type_len
                    bytlen -= byt_beg*type_len
                    shape_arr[-1] -= nbeg
                    if nend is not None:
                        bytlen = (nend - nbeg)*np.prod(shape_arr[:-1])*type_len
                        shape_arr[-1] = nend - nbeg

                self.data = np.ndarray(shape_arr, '>%s' %sfmt, getChunk(self.sfname, addr, bytlen), order='F')


    def ppg_time(self): # Bug MAG:27204
        """Returns the time-array in [s] for TB of type PPG_prog"""

        for robj in self.relobjects:
            if robj.objectType == oid.Device:
                ppg = robj.data # Device/ParSet dictionary
                npt = self.n_pre
                nsteps = self.n_steps
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
                nptyp = sfmap.typeMap('SFfmt', 'np', self.dataFormat)
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
                if len(time_ppg) != 0:
                    self.data = time_ppg[:nsteps]


    def time_last(self):
        """True if SigGroup has time as last coordinate"""

        if not hasattr(self, 'time_dim'):
            return False
        return (self.time_dim == self.num_dims-1)
