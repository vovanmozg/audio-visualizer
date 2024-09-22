ffmpeg -i ./files/effect_particles.mp4 -filter_complex \
"[0:v]trim=0:15,setpts=PTS-STARTPTS[v0]; \
 [v0]split=6[v0_1][v0_2][v0_3][v0_4][v0_5][v0_6]; \
 [v0_1][v0_2]xfade=transition=fade:duration=1:offset=14[v1]; \
 [v1][v0_3]xfade=transition=fade:duration=1:offset=28[v2]; \
 [v2][v0_4]xfade=transition=fade:duration=1:offset=42[v3]; \
 [v3][v0_5]xfade=transition=fade:duration=1:offset=56[v4]; \
 [v4][v0_6]xfade=transition=fade:duration=1:offset=70[v5]; \
 [v5]trim=duration=80[final]" \
 -map "[final]" -c:v libx264 -pix_fmt yuv420p ./files/effect_particles_looped.mp4 -y

ffmpeg -i ./files/example_color_shift.mp4 -i ./files/effect_particles_looped.mp4 -filter_complex \
"[1:v]scale=1792:1024,eq=brightness=0.5[particles]; \
 [1:v]scale=1792:1024,format=gray[alpha_mask]; \
 [particles][alpha_mask]alphamerge[particles_with_alpha]; \
 [0:v][particles_with_alpha]overlay=0:0:format=auto[out]" \
 -map "[out]" -map 0:a? -c:v libx264 -pix_fmt yuv420p \
 -c:a copy ./files/example_color_shift_with_effect.mp4 -y


# удлиление видео с эффектом
#ffmpeg -i ./files/effect_particles.mp4 -filter_complex \
#"[0:v]split[v1][v2]; \
# [v1]trim=0:14,setpts=PTS-STARTPTS[v1_trim]; \
# [v2]trim=1:15,setpts=PTS-STARTPTS[v2_trim]; \
# [v1_trim][v2_trim]xfade=transition=fade:duration=1:offset=13[looped]; \
# [looped]trim=duration=80[final]" \
# -map "[final]" -c:v libx264 -pix_fmt yuv420p ./files/effect_particles_looped.mp4
#
#
#ffmpeg -i ./files/example_color_shift.mp4 -stream_loop -1 -i ./files/effect_particles.mp4 -filter_complex \
#"[1:v]scale=1792:1024,eq=brightness=0.5[particles]; \
# [1:v]scale=1792:1024,format=gray[alpha_mask]; \
# [particles][alpha_mask]alphamerge[particles_with_alpha]; \
# [0:v][particles_with_alpha]overlay=0:0[out]" \
# -map "[out]" -map 0:a? -c:v libx264 -pix_fmt yuv420p \
# -c:a copy -shortest ./files/example_color_shift_with_effect.mp4
#
