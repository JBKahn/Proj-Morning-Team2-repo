// Path Helpers
var appPath = "static_src/";
var bowerPath =  "bower_components/";
var buildPath = "build/";
var staticPath = "static/";

var appConfig = {
    appName: "AbArticulusHomeApp",
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
                    appConfig.path.bowerPath + "jquery/dist/jquery.min.js",
                    appConfig.path.bowerPath + "bootstrap/dist/js/bootstrap.min.js"
                ],
                dest: appConfig.path.buildPath + "js/requirements.dist.js"
            },
            css: {
                src: [
                    appConfig.path.bowerPath + "bootstrap/dist/css/bootstrap.min.css",
                ],
                dest: appConfig.path.buildPath + "css/deps.style.dist.css"
            },
            jsDist: {
                src: [
                    appConfig.path.buildPath + "js/requirements.dist.js",
                    appConfig.path.appPath + "js/app.js"
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
                        src: [appConfig.path.bowerPath + "bootstrap/fonts/*"],
                        dest: appConfig.path.staticPath + '<%= appConfig.appName %>/fonts/', filter: "isFile"
                    }, {
                        expand: true,
                        flatten: true,
                        src: [appConfig.path.bowerPath + "jquery/dist/jquery.min.map"],
                        dest: appConfig.path.staticPath + '<%= appConfig.appName %>/js/', filter: "isFile"
                    },
                ]
            }
        },

        watch: {
            dev: {
                files: [
                    appPath + "sass/*",
                    appPath + "js/*",
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
        }
    });

    grunt.registerTask('default', ['sass', 'concat', 'copy']);
    grunt.registerTask('dev', ['default', 'watch']);

};
