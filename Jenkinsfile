pipeline {
  agent any
  stages {
    stage('Tests') {
      parallel {
        stage('Compile') {
          agent {docker {image 'python:3-alpine'}}
          steps {
            sh 'echo Hello World'
          }
        }
        stage('SonarQube') {
          steps{
            script{
              scannerHome = tool 'SonarQube 4.7';
            }
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
