# hc3.py
# helper functions to load data from CRCNS hc-3 repository

import os.path
import pandas as pd
import numpy as np
import re

from mymap import Map

def get_num_electrodes(sessiondir):
    numelec = 0
    files = [f for f in os.listdir(sessiondir) if (os.path.isfile(os.path.join(sessiondir, f)))]
    for ff in files:
        try:
            found = re.search('\.clu\.[0-9]+$', ff).group(0)
            numelec+=1
        except:
            found=''
    if numelec > 0:
        return numelec
    else:
        raise ValueError('number of electrodes (shanks) could not be established...')

#datatype = ['spikes', 'eeg', 'pos', '?']
def load_data(fileroot, animal='gor01', year=2006, month=6, day=7, session='11-26-53', datatype='spikes', channels='all', fs=32552,starttime=0, verbose=False):
    
    fileroot = os.path.normpath(fileroot)
    anim_prefix = "{}-{}-{}".format(animal,month,day)
    session_prefix = "{}-{}-{}_{}".format(year,month,day,session)
    sessiondir = "{}/{}/{}".format(fileroot, anim_prefix, session_prefix) 

    if (datatype=='spikes'):
        #filename = "{}/{}/{}/{}.clu.1".format(fileroot, anim_prefix, session_prefix, session_prefix) 
        filename = "{}/{}/{}/{}".format(fileroot, anim_prefix, session_prefix, session_prefix)
        #print(filename)
        if verbose:
            print("Loading data for session in directory '{}'...".format(sessiondir))
        num_elec = get_num_electrodes(sessiondir)
        if verbose:
            print('Number of electrode (.clu) files found:', num_elec)
        st_array = []
        # note: using pandas.read_table is orders of magnitude faster here than using numpy.loadtxt
        for ele in np.arange(num_elec):
            #%time dt1a = np.loadtxt( base_filename1 + '.clu.' + str(ele + 1), skiprows=1,dtype=int)
            eudf = pd.read_table( filename + '.clu.' + str(ele + 1), header=None, names='u' ) # read unit numbers within electrode
            tsdf = pd.read_table( filename + '.res.' + str(ele + 1), header=None, names='t' ) # read sample numbers for spikes
            max_units = eudf.u.values[0]
            eu = eudf.u.values[1:]
            ts = tsdf.t.values
            # discard units labeled as '0' or '1', as these correspond to mechanical noise and unsortable units
            ts = ts[eu!=0]
            eu = eu[eu!=0]
            ts = ts[eu!=1]
            eu = eu[eu!=1]
            
            for uu in np.arange(max_units-2):
                st_array.append(ts[eu==uu+2])

        if verbose:
            print('Spike times (in sample numbers) for a total of {} units were read successfully...'.format(len(st_array)))
        spikes = Map()
        spikes['data'] = st_array
        spikes['num_electrodes'] = num_elec
        spikes['num_units'] = len(st_array)
        spikes['samprate'] = fs
        spikes['session'] = session_prefix

        return spikes
    
        ## continue from here... we want to keep cells that are inactive in some, but not all environments...
        # hence when extracting info, we must take all sessions in a recording day into account, and not just a specific recording session
    
    elif (datatype=='eeg'):
        filename = "{}/{}/{}/{}.eeg".format(fileroot, anim_prefix, session_prefix, session_prefix)
        if verbose:
            print("Loading EEG data from file '{}'".format(filename))
        num_elec = get_num_electrodes(sessiondir)
        num_channels = num_elec*8
        if channels=='all':
            channels = list(range(0,num_channels))
        if verbose:
            print('Number of electrode (.clu) files found: {}, with a total of {} channels'.format(num_elec, num_channels))
        dtype = np.dtype([(('ch' + str(ii)), 'i2')  for ii in range(num_channels) ])
        # read eeg data:
        try:
            eegdata = np.fromfile(filename, dtype=dtype, count=-1)
        except:
            print( "Unexpected error:", sys.exc_info()[0] )
            raise
        num_records = len(eegdata)
        if verbose:
            print("Successfully read {} samples for each of the {} channel(s).".format(num_records, len(channels)))
        
        data_arr = eegdata.astype(dtype).view('i2')
        data_arr = data_arr.reshape(num_records,num_channels)
        eeg = Map()
        eeg['data'] = data_arr[:,channels]
        eeg['channels'] = channels
        eeg['samprate'] = fs
        eeg['starttime'] = starttime
        eeg['session'] = session_prefix
        
        return eeg

    elif (datatype=='pos'):
        filename = "{}/{}/{}/{}.whl".format(fileroot, anim_prefix, session_prefix, session_prefix)
        print("reading position data from '{}'".format(filename))
        dfwhl = pd.read_table(filename,sep='\t', skiprows=0, names=['x1', 'y1', 'x2', 'y2'] )
        return dfwhl
    else:
        raise ValueError('datatype is not handled')
        
def get_recording_days_for_animal(fileroot, animal):
    return [name for name in os.listdir(fileroot) if (os.path.isdir(os.path.join(fileroot, name))) & (name[0:len(animal)]==animal)]

def get_sessions_for_recording_day(fileroot, day):
    fileroot = os.path.join(fileroot,day)
    return [session for session in os.listdir(fileroot) if (os.path.isdir(os.path.join(fileroot, session)))]

def get_sessions(fileroot, animal='gor01', verbose=True):
    sessiondf = pd.DataFrame(columns=('animal','day','session','task'))
    fileroot = os.path.normpath(fileroot)
    if verbose:
        print("reading recording sessions for animal '{}' in directory '{}'...\n".format(animal,fileroot))
    for day in get_recording_days_for_animal(fileroot, animal):
        mm,dd = day.split('-')[1:]
        anim_prefix = "{}-{}-{}".format(animal,mm,dd)
        shortday = '-'.join([mm,dd])
        for session in get_sessions_for_recording_day(fileroot, day):
            infofile = "{}/{}/{}/{}.info".format(fileroot, anim_prefix, session, session)
            descr = ''
            try:
                with open(infofile, 'r') as f:
                    line = f.read()
                    if line.split('=')[0].strip()=='task':
                        descr = line.split('=')[-1].strip()
                if (descr == '') and (verbose == True):
                    print('Warning! Session type could not be established...')
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except ValueError:
                print ("Could not convert data to an integer.")
            except:
                print ("Unexpected error:", sys.exc_info()[0])
                raise
            session_hhmmss = session.split('_')[-1]
            sessiondf = sessiondf.append(pd.DataFrame({'animal':[animal],'day':[shortday],'session':[session_hhmmss],'task':[descr]}),ignore_index=True)
    if verbose:
        print(sessiondf)
    return sessiondf    

