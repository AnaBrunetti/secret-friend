const gulp = require('gulp'),
    rename = require('gulp-rename'),
    notify = require('gulp-notify'),
    sass = require('gulp-sass')(require('sass')),
    sourcemaps = require('gulp-sourcemaps'),
    browserSync = require('browser-sync'),
    reload = browserSync.reload,
    exec = require('child_process').exec;


const destPath = './website/static/',
    destSass = destPath + 'css/',
    destJs = destPath + 'js/',
    destImg = destPath + 'img/';

const devPath = './website/static_src/',
    devSass = devPath + 'scss/**/*.scss',
    devJs = devPath + 'js/*.js',
    devImg = devPath + 'img/**/*.{gif,png,jpg,jpeg,svg}';


// SASS files
gulp.task('style', async function () {
    gulp.src(devSass)
        .pipe(sourcemaps.init())
        .pipe(sass({ outputStyle: 'compressed' }).on('error', sass.logError))
        .on('error', notify.onError(function () {
            return 'Error on SASS/SCSS.\nLook in the console for details.\n';
        }))
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('./maps'))
        .pipe(gulp.dest(destSass))
        .on('end', function () {
            notify().write('Gulp Style Done')
        });
});

// JS Files
gulp.task('js', async function (cb) {
    gulp.src(devJs)
        .pipe(
            gulp.dest(destJs)
                .on('end', function () {
                    notify().write('Gulp JS Done')
                })
        )
});

// Images
gulp.task('images', async function () {
    return gulp.src(devImg)
        .pipe(gulp.dest(destImg))
        .on('end', function () {
            notify().write('Gulp Images Done')
        });
});

gulp.task('watch', function () {
    gulp.watch(devSass, ['style']);
    gulp.watch(devJs, ['js']);
});

gulp.task('watch:img', function () {
    gulp.watch(devImg, ['images']);
});

gulp.task('manage-py', function (callback) {

    exec('python manage.py collectstatic --no-input',
        function (err, stdout, stderr) {
            // console.log(stdout);
            // console.log(stderr);
            callback(err);
        });
    notify().write('Gulp manage-py Done!');
});

gulp.task('auto', function () {
    browserSync.init({
        notify: true,
        proxy: "localhost:8000"
    });
    gulp.watch([devPath + '**/*' + '.{scss,css,html,py,js}'], gulp.series(['style', 'js', 'images', 'manage-py']))
        .on('change', reload);
});

gulp.task('default', async function () {
    console.log('********************************************');
    console.log('*---====       BODE GULP HELP       ====---*');
    console.log('********************************************');
    console.log('Tasks:');
    console.log('- gulp style           SASS to CSS');
    console.log('- gulp js              JS compression');
    console.log('- gulp images          Images compression');
    console.log('- gulp watch           Watch for SASS and JS');
    console.log('- gulp watch:img       Watch for Images');
    console.log('- gulp manage-py       Call collectstatic');
    console.log('- gulp reload          Site reload auto');
    console.log('- gulp auto            Make all auto');
    console.log('********************************************');
});