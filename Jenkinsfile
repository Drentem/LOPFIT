pipeline {
  agent none
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
          SonarQube.execute(this, bparams)
        }
      }
    }
  }
}
