// Path Helpers
var appPath = "static_src/";
var bowerPath =  "bower_components/";
var buildPath = "build/";
var staticPath = "static/";

var appConfig = {
    appName: "TimeTableApp",
    path: {
        appPath: appPath,
        bowerPath:  bowerPath,
        buildPath: buildPath,
        staticPath: staticPath
    }
};

module.exports = function(grunt) {
    require('load-grunt-tasks')(grunt);
    grunt.initConfig({
        appConfig: appConfig,
        concat: {
            js: {
                src: [
                    appConfig.path.bowerPath + 'moment/min/moment-with-locales.js',
                    appConfig.path.bowerPath + "jquery/dist/jquery.min.js",
                    appConfig.path.bowerPath + "jquery-ui/jquery-ui.js",
                    appConfig.path.appPath + "js/fullcalendar.old.js",
                    appConfig.path.bowerPath + 'angular/angular.js',
                    appConfig.path.bowerPath + 'angular-route/angular-route.js',
                    appConfig.path.bowerPath + "bootstrap/dist/js/bootstrap.min.js",
                    appConfig.path.bowerPath + "angular-ui-calendar/src/calendar.js",
                    appConfig.path.bowerPath + "angular-bootstrap/ui-bootstrap-tpls.min.js",
                    appConfig.path.bowerPath + "ui-bootstrap/src/modal.js",
                    appConfig.path.bowerPath + "angular-animate/angular-animate.min.js",
                    appConfig.path.bowerPath + "angular-aria/angular-aria.min.js",
                    appConfig.path.bowerPath + "hammerjs/hammer.js",
                    appConfig.path.appPath + "js/angular-material.js"
                ],
                dest: appConfig.path.buildPath + "js/requirements.dist.js"
            },
            css: {
                src: [
                    appConfig.path.bowerPath + "bootstrap/dist/css/bootstrap.min.css",
                    appConfig.path.bowerPath + "font-awesome/css/font-awesome.min.css",
                    appConfig.path.bowerPath + "fullcalendar/dist/fullcalendar.css",
                    appConfig.path.bowerPath + "fullcalendar/fullcalendar.css",
                    appConfig.path.bowerPath + "ui-bootstrap/docs/css/style.css",
                    appConfig.path.bowerPath + "angular-material/angular-material.min.css"
                ],
                dest: appConfig.path.buildPath + "css/deps.style.dist.css"
            },
            angularApp: {
                src: [
                    appConfig.path.appPath + "js/app.js",
                    appConfig.path.appPath + "js/services/*.js",
                    appConfig.path.appPath + "js/controllers/*.js",
                    appConfig.path.appPath + "js/directives/*.js",
                    appConfig.path.appPath + "js/filters.js"
                ],
                dest: appConfig.path.buildPath + "js/" + appConfig.appName + ".app.js"
            },
            jsDist: {
                src: [
                    appConfig.path.buildPath + "js/requirements.dist.js",
                    appConfig.path.buildPath + "js/" + appConfig.appName + '.templates.js',
                    appConfig.path.buildPath + "js/" +  appConfig.appName + ".app.js"
                ],
                dest: appConfig.path.staticPath + '<%= appConfig.appName %>/js/<%= appConfig.appName %>.dist.js'
            },
            cssDist: {
                src: [
                  appConfig.path.buildPath + "css/deps.style.dist.css",
                  appConfig.path.buildPath + "css/app.css"
                ],
                dest: appConfig.path.staticPath + '<%= appConfig.appName %>/css/<%= appConfig.appName %>.dist.css'
            }
        },

        copy: {
            main: {
                files: [
                    // includes files within path
                    {
                        expand: true,
                        flatten: true,
                        src: [appConfig.path.buildPath + "css/app.css.map"],
                        dest: appConfig.path.staticPath + '<%= appConfig.appName %>/css/', filter: "isFile"
                    }, {
                        expand: true,
                        flatten: true,
                        src: [appConfig.path.bowerPath + "font-awesome/fonts/*"],
                        dest: appConfig.path.staticPath + '<%= appConfig.appName %>/fonts/', filter: "isFile"
                    }, {
                        expand: true,
                        flatten: true,
                        src: [appConfig.path.bowerPath + "bootstrap/fonts/*"],
                        dest: appConfig.path.staticPath + '<%= appConfig.appName %>/fonts/', filter: "isFile"
                    }, {
                        expand: true,
                        flatten: true,
                        src: [appConfig.path.bowerPath + "jquery/dist/jquery.min.map"],
                        dest: appConfig.path.staticPath + '<%= appConfig.appName %>/js/', filter: "isFile"
                    }, {
                        expand: true,
                        flatten: true,
                        src: [appConfig.path.bowerPath + "jquery/dist/jquery.js"],
                        dest: appConfig.path.staticPath + '<%= appConfig.appName %>/js/', filter: "isFile"
                    }
                ]
            }
        },

        watch: {
            dev: {
                files: [
                    appPath + "sass/*",
                    appPath + "js/*",
                    appPath + "templates/*",
                ],
                tasks: ['default']
            }
        },

        sass: {
            dist: {
                files: {
                    "build/css/app.css": appPath + "sass/style.scss",
                },
                options: {
                    sourcemap: "inline",
                }
            }
        },

        ngtemplates: {
            templates: {
                cwd: appConfig.path.appPath,
                options: {
                    module: "AppTemplates",
                    standalone: true
                },
                src: "templates/**.html",
                dest: appConfig.path.buildPath + "js/" + appConfig.appName + ".templates.js"
            }
        }
    });

    grunt.registerTask('default', ['sass', 'ngtemplates', 'concat', 'copy']);
    grunt.registerTask('dev', ['default', 'watch']);

};
