pipeline {
  agent none
  stages {
    stage('Tests') {
      parallel {
        stage('Compile') {
          agent {
            node {
              label 'Local Agent 1'
            }

          }
          steps {
            sh 'python3 -m compileall .'
            stash(name: 'compiled-results', includes: '**/*.py*')
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

    stage('Package') {
      parallel {
        stage('macOS') {
          steps {
            echo 'Cannot Compile. Need a Mac'
          }
        }

        stage('Windows') {
          steps {
            echo 'Need Windows agent'
          }
        }

      }
    }

  }
}