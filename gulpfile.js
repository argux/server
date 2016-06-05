var gulp = require('gulp');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var pump = require('pump');
var clean_css = require('gulp-clean-css');

gulp.task('concatenate_js_lib', function() {
    pump([
        gulp.src([
            'argux_server/static/js/lib/source/version.js',
            'argux_server/static/js/lib/source/rest.js',
            'argux_server/static/js/lib/source/global_chart_configs.js',
            'argux_server/static/js/lib/source/host.js',
            'argux_server/static/js/lib/source/monitors.js',
            'argux_server/static/js/lib/source/user.js',
            'argux_server/static/js/lib/source/graph.js',
            'argux_server/static/js/lib/source/timeframe.js'
        ]),
        concat('argux.js'),
        gulp.dest('argux_server/static/js/lib/debug')
    ]);
});

gulp.task('minify_js_lib', ['concatenate_js_lib'], function() {
    pump([
        gulp.src('argux_server/static/js/lib/debug/*.js'),
        uglify(),
        gulp.dest('argux_server/static/js/lib/')
    ]);
});

gulp.task('concatenate_js', function() {
    pump([
        gulp.src([
            'argux_server/static/js/source/overview.js'
        ]),
        concat('overview.js'),
        gulp.dest('argux_server/static/js/debug')
    ]);
});

gulp.task('minify_js', ['concatenate_js'], function() {
    pump([
        gulp.src('argux_server/static/js/debug/overview.js'),
        uglify(),
        gulp.dest('argux_server/static/js')
    ]);
});

gulp.task('concatenate_css', function() {
    pump([
        gulp.src([
            'argux_server/static/css/source/theme.css',
        ]),
        concat('argux.css'),
        gulp.dest('argux_server/static/css/debug')
    ]);
});

gulp.task('minify_css', ['concatenate_css'], function() { pump([
        gulp.src('argux_server/static/css/debug/argux.css'),
        clean_css(),
        gulp.dest('argux_server/static/css')
    ]);
});

gulp.task('default', ['minify_js', 'minify_css', 'minify_js_lib']);
