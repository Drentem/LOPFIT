pipeline {
  agent any
  stages {
    stage('Compile') {
      agent {docker {image 'python:3-alpine'}}
      steps {
        sh 'python -m compileall .'
        stash(name: 'compiled-results', includes: '**/*.py*')
      }
    }
    stage('Tests') {
      parallel {
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
