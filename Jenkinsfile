pipeline {
  agent any
  stages {
    stage('Tests') {
      parallel {
        stage('Compile') {
          agent {
            docker {image 'python:2-alpine'}
          }
          steps {
            sh 'compileall'
            stash(name: 'compiled-results', includes: '**/*.py*')
          }
        }
        stage('SonarQube') {
          agent{ label 'Local Agent 1'}
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
