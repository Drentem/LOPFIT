pipeline {
  agent any
  stages {
    stage('Tests') {
      parallel {
        stage('Compile') {
          agent {docker {image 'python:3-alpine'}}
          steps {
            sh 'python -m py_compile **.py'
            stash(name: 'compiled-results', includes: '**.py*')
          }
        }
        stage('SonarQube') {
          steps {
            withSonarQubeEnv('SonarQube') {
              sh "./sonar-scanner"
            }
          }
        }
        stage('SonarQube analysis') {
          def scannerHome = tool 'SonarScanner 4.0';
          steps{
            withSonarQubeEnv('SonarQube') {
              sh "${scannerHome}/bin/sonar-scanner"
            }
          }
        }
      }
    }
    stage('Quality Gate') {
      steps{
        waitForQualityGate abortPipeline: true
      }
    }
  }
}
