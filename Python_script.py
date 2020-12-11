#!/usr/bin/env python3

import grass.script as gscript


def main():
    dists = [250, 500, 1000, 2500, 5000]

    for dist in dists:
        gscript.run_command('g.region', flags='p', vector='motorways@PERMANENT')
        gscript.run_command('v.buffer', input='motorways@PERMANENT', output='motorways_pyth_'+str(dist), distance=dist)
        gscript.run_command('v.to.rast', input='motorways_pyth_'+str(dist), output='motorways_rasterized_pyth_'+str(dist), use='v')
        gscript.run_command('r.stats.zonal', base='motorways_rasterized_pyth_'+str(dist), cover='GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3@PERMANENT', method='sum', output='districts_bw_pop_motorways_sum_pyth_'+str(dist))
        gscript.run_command('r.stats', input='districts_bw_pop_motorways_sum_pyth_'+str(dist))

if __name__ == '__main__':
    main()
