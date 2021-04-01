#! groovy

@Library('gcs-build-scripts@debian-cowbuilder-init') _

pipeline {
    agent none
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        parallelsAlwaysFailFast()
        timeout(time: 3, unit: 'HOURS')
    }
    stages {
        stage ("Checkout") {
            agent any
            steps {
                checkout scm
            }
        }
        stage ("libs3 (w/Globus modifications)") {
            steps {
                script {
                    env.EPIC = 2729
                    automakePipeline()
                }
            }
        }
    }
}
