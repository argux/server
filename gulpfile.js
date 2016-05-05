var gulp = require('gulp');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var pump = require('pump');

gulp.task('concatenate_js', function() {
    pump([
        gulp.src([
            'argux_server/static/js/source/overview.js',
        ]),
        concat('overview.js'),
        gulp.dest('argux_server/static/js/debug')
    ]);
    pump([
        gulp.src([
            'argux_server/static/js/lib/source/version.js',
            'argux_server/static/js/lib/source/rest.js',
            'argux_server/static/js/lib/source/global_chart_configs.js',
            'argux_server/static/js/lib/source/host.js',
        ]),
        concat('argux.js'),
        gulp.dest('argux_server/static/js/lib/debug')
    ]);
});

gulp.task('minify_js', ['concatenate_js'], function() {
    pump([
        gulp.src('argux_server/static/js/lib/debug/argux.js'),
        uglify(),
        gulp.dest('argux_server/static/js/lib/')
    ]);
    pump([
        gulp.src('argux_server/static/js/debug/overview.js'),
        uglify(),
        gulp.dest('argux_server/static/js/')
    ]);
});

gulp.task('default', ['minify_js']);
