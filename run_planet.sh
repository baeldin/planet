#!/bin/bash
#Usage: planet [options]
# 
#options:
#  -?                (or any illegal option) Output this text
#  -s seed           Specifies seed as number between 0.0 and 1.0
#  -w width          Specifies width in pixels, default = 800
#  -h height         Specifies height in pixels, default = 600
#  -m magnification  Specifies magnification, default = 1.0
#  -o output_file    Specifies output file, default is standard output
#  -l longitude      Specifies longitude of centre in degrees, default = 0.0
#  -L latitude       Specifies latitude of centre in degrees, default = 0.0
#  -g gridsize       Specifies vertical gridsize in degrees, default = 0.0 (no grid)
#  -G gridsize       Specifies horisontal gridsize in degrees, default = 0.0 (no grid)
#  -i init_alt       Specifies initial altitude (default = -0.02)
#  -c                Colour depends on latitude (cumulative, default: only altitude)
#  -C file           Read colour definitions from file
#  -O                Produce a black and white outline map
#  -E                Trace the edges of land in black on colour map
#  -B                Use ``bumpmap'' shading
#  -b                Use ``bumpmap'' shading on land only
#  -d                Use ``daylight'' shading
#  -a angle	      Angle of ``light'' in bumpmap shading
#                    or longitude of sun in daylight shading
#  -A latitude	      Latitude of sun in daylight shading
#  -P                Use PPM file format (default is BMP)
#  -x                Use XPM file format (default is BMP)
#  -H                Write heightfield (default is BMP)
#  -M                Use match sketch (see manual)
#  -V number         Distance contribution to variation (default = 0.03)
#  -v number         Altitude contribution to variation (default = 0.4)
#  -pprojection      Specifies projection: m = Mercator (default)
#                                          p = Peters
#                                          q = Square
#                                          s = Stereographic
#                                          o = Orthographic
#                                          g = Gnomonic
#                                          a = Area preserving azimuthal
#                                          c = Conical (conformal)
#                                          M = Mollweide
#                                          S = Sinusoidal
#                                          i = Icosaheral
#                                          h = Heightfield (obsolete)
set -x
seed=49
#        seeed      filename         zoom  width   height  lon   lat   lon0   lat0   proj
./planet -s ${seed} -o ${seed}.bmp            -w 2000 -h 1000 -g 10 -G 10               -p M -n &
./planet -s ${seed} -o ${seed}_N.bmp          -w 2000 -h 1000 -g 30 -G 30        -L  90 -p M -n &
./planet -s ${seed} -o ${seed}_S.bmp          -w 2000 -h 1000 -g 30 -G 30        -L -90 -p M -n &
./planet -s ${seed} -o ${seed}_1.bmp -m 3     -w 2000 -h 1000 -g 10 -G 10                    -n
./planet -s ${seed} -o ${seed}_2.bmp -m 6     -w 2000 -h 1000 -g 10 -G 10 -l  30 -L 15       -n &
./planet -s ${seed} -o ${seed}_3.bmp -m 6     -w 2000 -h 1000 -g 10 -G 10 -l  30 -L -15      -n &
./planet -s ${seed} -o ${seed}_4.bmp -m 45    -w 2000 -h 1000 -g  5 -G  5 -l  30 -L -15      -n &
./planet -s ${seed} -o ${seed}_s.bmp -m 20    -w 1000 -h 1000 -g  5 -G  5 -l 110 -L -45 -p s -n
./planet -s ${seed} -o ${seed}.asc   -m 1     -w 1000 -h 500                            -p q -n -H&
wait