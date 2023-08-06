#! /usr/bin/env python
import os
import glob
import numpy as np

from casacore import tables

parser = ArgumentParser("Convert sage solutions to numpy");

parser.add_argument('-ms_list','--obsid',help='obs Id',dest="obsid",required=True)
parser.add_argument('-m','--MS',nargs="+",help='MS for metadata',dest="MS",required=True)
parser.add_argument('-c','--cluster', nargs=2, help='cluster indices (start,end)',dest='cluster',default=[0,1],type=int)
parser.add_argument('-p','--indir', help='directory for the input',dest='indir',default="/data/users/lofareor/sarod/pipeline/")
parser.add_argument('--pid',type=int, help='process step id (default =2)',dest='pid',default=2) 
parser.add_argument('--post',type=str, help='postfix (e.g. _NP)',dest='post',default='')
parser.add_argument('-d','--outdir', help='directory for the output',dest='outdir',default="/net/node131/data/users/lofareor/NCP/numpy_data/")
parser.add_argument('-n','--nodelist', nargs='+',help='nodes. On EOR-cluster: specify consecutive multiple nodes as e.g. 116..131 (will use \'node116\' to \node\'131)',dest="nodelist",default=[os.getenv('HOSTNAME')])

def get_ms_info(ms_file):
    ms=tables.table(ms_file)

    timerange = [np.amin(ms.getcol('TIME_CENTROID')), np.amax(ms.getcol('TIME_CENTROID'))]
    timestep = ms.getcell('INTERVAL', 0)
    
    pointing = tables.table(ms.getkeyword('FIELD')).getcell('PHASE_DIR', 0);    
    stations = tables.table(ms.getkeyword('ANTENNA')).getcol('NAME')
    station_pos = tables.table(ms.getkeyword('ANTENNA')).getcol('POSITION')

    return (timerange, timestep, pointing.flatten(), stations, station_pos)



@click.command()
@click.version_option(__version__)
@click.argument('ms_list', type=str)
@click.argument('out_dir', type=str)
def main(ms_list, out_dir):
    alldatas = []
    freqs = []
    ms_files = [k.strip().split() for k in open(ms_list).readlines() if k.strip()]
    obs_id = os.path.basename(ms_files[0]).strip('_')[0]
    ms_sols = [k + '.solutions' for k in ms_files]

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    
    timerange, timestep, pointing, stations, station_pos = get_ms_info(ms_files[0])
    
    for ms_sol in ms_sols:
        with open(ms_sol) as f:
            for i in range(3):
                a = f.readline()
            freq, bw, timestep, nStations, nClust, nClustEff = tuple([float(i) for i in a.split()])
        data = np.loadtxt(fname, skiprows=3, usecols=tuple(range(1, int(nClustEff) + 1)), unpack=True)
        datas = []
        for i in range(int(nClustEff)):
            a = data[i].reshape((-1, int(nStations), 4, 2))
            cdata = a[:, :, :, 0] + 1.j * a[:, :, :, 1]
            datas.append(cdata)
        freqs.append(freq)
        alldatas.append(datas)
    
    mysorted = zip(*sorted(zip(freqs, alldatas)))

    cdata = (np.array(mysorted[1])[:, args.cluster[0]:args.cluster[1]]).transpose((2, 3, 0, 4, 1))
    data = np.zeros(cdata.shape + (2,), dtype=np.float64)
    data[:, :, :, :, :, 0] = np.real(cdata)
    data[:, :, :, :, :, 1] = np.imag(cdata)
    timestep = (timerange[1] - timerange[0]) / (data.shape[0] - 1)

    np.savez("%s/%s" % (out_dir, obs_id),
            freqs=np.array(mysorted[0]) * 1.e6, 
            timerange=timerange, 
            timestep=timestep, 
            stations=stations, 
            stat_pos=station_pos, 
            pointing=pointing)
    np.save("%s/%s" % (out_dir, obs_id), data)

if __name__ == '__main__':
    main()
