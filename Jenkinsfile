pipeline {
  agent none
  stages {
    stage('Tests') {
      parallel {
        stage('Compile') {
          agent {
            docker {
              image 'python:3-alpine'
            }

          }
          steps {
            sh 'compileall'
            stash(name: 'compiled-results', includes: '**/*.py*')
            timeout(time: 60) {
              error 'Compile timeout'
            }

          }
        }

        stage('SonarQube') {
          agent any
          steps {
            script {
              scannerHome = tool 'SonarQube 4.7'
            }

            withSonarQubeEnv('SonarQube') {
              sh "${scannerHome}/bin/sonar-scanner"
            }

          }
        }

      }
    }

    stage('Quality Gate') {
      steps {
        waitForQualityGate true
      }
    }

  }
}