var gulp = require('gulp');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var pump = require('pump');

gulp.task('concatenate_js', function() {
    pump([
        gulp.src([
            'argux_server/static/js/source/version.js',
            'argux_server/static/js/source/rest.js',
            'argux_server/static/js/source/global_chart_configs.js',
            'argux_server/static/js/source/host.js',
        ]),
        concat('argux.js'),
        gulp.dest('argux_server/static/js/debug')
    ]);
});

gulp.task('minify_js', ['concatenate_js'], function() {
    pump([
        gulp.src('argux_server/static/js/debug/argux.js'),
        uglify(),
        gulp.dest('argux_server/static/js/')
    ]);
});

gulp.task('default', ['minify_js']);
