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
      container('docker'){
        try {
          stage('Build Prep'){
            catchError( stageResult: 'SUCCESS'){ 
//              hubotSend message: "Build ${JOB_NAME} has Started,\n Build Number ${BUILD_ID},\n More infomation @ ${BUILD_URL}\n ", url: 'http://jenkins-bot.bots.svc.cluster.local:8080', room: "#jenkins", failOnError: 'true', tokens: "BUILD_NUMBER,BUILD_ID", status: 'STARTED'
            }
            sh 'apk add make git npm'
            sh 'git config --global --add safe.directory $(pwd)'  // Workaround for https://github.blog/2022-04-12-git-security-vulnerability-announced/
            sh 'export'
            sh 'echo listing plugins '
            this.npmPluginsRaw = sh(script:"echo \"${npmPlugins}\"", returnStdout: true).trim()
            this.npmPlugins = this.npmPluginsRaw.split("\\r?\\n")
            // for ( i=0; i<this.npmPlugins.size(); i++){
            //   key = this.npmPlugins[i].split("plugins-")
            //   key2 = key[1].capitalize()
            //   sh "echo key = ${key[1]}  ${key2}"
            // }
            
          }
          stage('Github Clone'){
            git changelog: false, credentialsId: 'Jenkins-ssh', poll: false, url: 'https://github.com/switchdin/superset.git', branch: branch
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
          
          /*
          stage('Setup npm for Docker'){
            // sh "npm config set cache /opt/jenkins/.npm"
            sh 'npm config set strict-ssl false'
            sh "npm config set registry https://helm.k8s.switchdinlocal/repository/npm-group/"
            sh "npm set //helm.k8s.switchdinlocal/repository/npm-group/:_authToken NpmToken.b913ef90-29ed-3062-9508-a0fd62f3830f"
            sh 'cp /root/.npmrc npmrc -v && chown 1000.1000 npmrc'
            sh 'sed "/AS superset-node/a COPY npmrc /app/superset-frontend/.npmrc" -i Dockerfile'
          }
          */
          
          /* You started you comment out here Bailey 1-3-22
          
          stage ('Add Custom components'){
            for ( i=0; i<this.npmPlugins.size(); i++){
              sh "echo plugin: ${this.npmPlugins[i]}"
              // sh 'cd superset-frontend  && NODE_OPTIONS=--max_old_space_size=8192 npm install  @switchdin-superset-plugins/core'
              sh "sysctl -w vm.max_map_count=655300"
              sh "cd superset-frontend  && NODE_OPTIONS=--max_old_space_size=16384 npm install  @switchdin-superset-plugins/${this.npmPlugins[i]}"
            }
          }
          stage ('inject compnenets into setupPluginsExtra'){
            // empty file
            sh 'echo > superset-frontend/src/setup/setupPluginsExtra.ts'
            //setup imports
            for ( i=0; i<this.npmPlugins.size(); i++){
              key0  =   this.npmPlugins[i].split("@")
              key = key0[0].split("plugins-")
              key2 = key[1].capitalize()
              sh "echo \"import SwitchdinPlugin${key2} from '@switchdin-superset-plugins/switchdin-superset-plugins-${key[1]}';\" >> superset-frontend/src/setup/setupPluginsExtra.ts "
            }
            sh "echo 'export default function setupPluginsExtra() {' >> superset-frontend/src/setup/setupPluginsExtra.ts "
            // setup configuration
            for ( i=0; i<this.npmPlugins.size(); i++){  
              key0  =   this.npmPlugins[i].split("@")
              key = key0[0].split("plugins-")
              key2 = key[1].capitalize()
              sh "echo \"     new SwitchdinPlugin${key2}().configure({key: '${key[1]}'}).register();\" >> superset-frontend/src/setup/setupPluginsExtra.ts "
            }            
            sh "echo '}'>> superset-frontend/src/setup/setupPluginsExtra.ts "
            sh "cat superset-frontend/src/setup/setupPluginsExtra.ts"
            
          */ //You commented out to here Bailey - 1-3-22 (also the bracket before stage 'Docker Build' on line 120)
          
            // sh "sed \"/import WorldMapChartPlugin.*/a import ComposedChartPlugin from '@switchdin-superset-plugins/plugin-chart-composed';\" -i superset-frontend/src/visualizations/presets/MainPreset.js"
            // sh "sed \"/new AreaChartPlugin/i         new ComposedChartPlugin().configure({ key: 'composed' }),\" -i superset-frontend/src/visualizations/presets/MainPreset.js"
            // sh "sed 's/^new ComposedChartPlugin/        new ComposedChartPlugin/g' -i superset-frontend/src/visualizations/presets/MainPreset.js"
          //}
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