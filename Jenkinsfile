// check out code
stage name: 'check-out-code'

node('slave') {
    dir('src') {
        checkout scm
    }
    stash 'src'
}


// make sure the containers can build
stage name: 'attempt-build-images'

node('slave') {
    unstash 'src'
    dir('src') {
        sh 'make build'
    }
}


// deploy to prod
if (env.BRANCH_NAME == 'master') {
    stage name: 'build-without-cache-and-push-images'
    dir('src') {
        sh 'make push'
    }
}


// vim: ft=groovy
