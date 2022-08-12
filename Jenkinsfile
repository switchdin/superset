def call(Map args) {
  def containers = [
    containerTemplate(
      args: 'cat', 
      command: '/bin/sh -c', 
      image: 'docker:dind',
      name: 'docker', 
      ttyEnabled: true,
      privileged: true,
      workingDir: '/home/jenkins/agent'
    ),
    containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent:4.3-4', ttyEnabled: true)
  ]
  def volumes = [
      hostPathVolume(
        hostPath: '/var/run/docker.sock', 
        mountPath: '/var/run/docker.sock'
      ),
      persistentVolumeClaim(
        claimName: 'node-pv-claim', 
        mountPath: '/opt/jenkins/.npm', 
        readOnly: false
      )
    ]
  
  def name = args.name.replace(" ","-").trim()
  def branch = args.branch.replace(" ","-").trim()
  def label = name

  podTemplate(label: label, containers: containers, volumes: volumes) {
    node(label) {
      checkout scm
      container('docker'){
        try {
          stage('Build Prep'){
            catchError( stageResult: 'SUCCESS'){ 
//              hubotSend message: "Build ${JOB_NAME} has Started,\n Build Number ${BUILD_ID},\n More infomation @ ${BUILD_URL}\n ", url: 'http://jenkins-bot.bots.svc.cluster.local:8080', room: "#jenkins", failOnError: 'true', tokens: "BUILD_NUMBER,BUILD_ID", status: 'STARTED'
            }
            sh 'apk add git npm'
            sh 'git config --global --add safe.directory $(pwd)'  // Workaround for https://github.blog/2022-04-12-git-security-vulnerability-announced/
            this.username = sh (
            script: 'git --no-pager show -s --format=\'%ae\' | cut -d@ -f1',
            returnStdout: true
          ).trim()
            sh 'export'
            sh 'echo listing plugins '
            this.npmPluginsRaw = sh(script:"echo \"${npmPlugins}\"", returnStdout: true).trim()
            this.npmPlugins = this.npmPluginsRaw.split("\\r?\\n")
          }
          // stage('build testing'){
          //     sh 'ls -l'
          //   sh 'find |grep setupPluginsExtra'
          //   // empty file
          //   sh 'echo > superset-frontend/src/setup/setupPluginsExtra.ts'
          //   //setup imports
          //   for ( i=0; i<this.npmPlugins.size(); i++){  
          //     key = this.npmPlugins[i].split("plugins-")
          //     key2 = key[1].capitalize()
          //     sh "echo \"import SwitchdinPlugin${key2} from 'switchdin-superset-plugins-${key[1]}';\" >> superset-frontend/src/setup/setupPluginsExtra.ts "
          //   }
          //   sh "echo 'export default function setupPluginsExtra() {' >> superset-frontend/src/setup/setupPluginsExtra.ts "
          //   // setup configuration
          //   for ( i=0; i<this.npmPlugins.size(); i++){  
          //     key = this.npmPlugins[i].split("plugins-")
          //     key2 = key[1].capitalize()
          //     sh "echo \"     new SwitchdinPlugin${key2}().configure({key: '${key[1]}'});\" >> superset-frontend/src/setup/setupPluginsExtra.ts "
          //   }            
          //   sh "echo '}'>> superset-frontend/src/setup/setupPluginsExtra.ts "
          //   sh "cat superset-frontend/src/setup/setupPluginsExtra.ts"

          // }
          stage('Docker Build') {
            this.ver = "ecr.aws.switchdinlocal/switchdin/superset:${branch}-${BUILD_ID}"
            this.latest = "ecr.aws.switchdinlocal/switchdin/superset:latest"
            this.test_image = "docker-push.k8s.switchdinlocal/test/switchdin/superset:latest"
            currentBuild.description=this.ver
            sh "docker build -t ${this.ver} . "
            sh "docker tag ${this.ver} ${this.latest}"
            sh "docker tag ${this.ver} ${this.test_image}"
          }
          stage('Push Image for Scan'){
            sh "echo 'vRMzx8T4PT9OEAdFADwQZ' |docker login --username jenkins --password-stdin docker-push.k8s.switchdinlocal"
            sh "docker push ${this.test_image}"
          }
          stage('Analyse Image') {
            try {
              sh "echo ${this.test_image} Dockerfile > VERSION"
              anchore forceAnalyze: true,name: 'VERSION',bailOnFail: false, bailOnPluginFail: false
            } catch (Exception err) {
              echo "Anchore failed: ${err}"
              currentBuild.result = 'FAILURE'
//               hubotSend message: "Build ${JOB_NAME} FAILED,\n Anchore image test issues\n More infomation @ ${BUILD_URL}\n ", url: 'http://jenkins-bot.bots.svc.cluster.local:8080', room: "#jenkins", failOnError: 'true', tokens: "BUILD_NUMBER,BUILD_ID", status: 'STARTED'
            }
          }
          stage('Push to Repo'){
            sh "docker push ${this.ver}"
            sh "docker push ${this.latest}"
            catchError( stageResult: 'SUCCESS'){ 
//              hubotSend message: "Build ${JOB_NAME} has finsish,\n Built container ${this.ver},\n More infomation @ ${BUILD_URL}\n ", url: 'http://jenkins-bot.bots.svc.cluster.local:8080', room: "#jenkins", failOnError: 'true', tokens: "BUILD_NUMBER,BUILD_ID", status: 'STARTED'
            }
                    
          }
        } catch (Exception e){
          catchError( stageResult: 'FAILURE'){ 
//              hubotSend message: "Build ${JOB_NAME} FAILED,\n More infomation @ ${BUILD_URL}\n ", url: 'http://jenkins-bot.bots.svc.cluster.local:8080', room: "#jenkins", failOnError: 'true', tokens: "BUILD_NUMBER,BUILD_ID", status: 'STARTED'
            }
        }
      }
    }
  }
}

call( name: env.JOB_NAME.trim().replace("/","-"), branch: env.branch )