<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>
          <img src="../assets/fortune-cookie.png" alt="fortune cookie" height="42" width="42">
          Fortunes
        </h1>
        <hr>
        <button id="add-fortune-button" type="button" class="btn btn-success btn-sm" v-b-modal.fortune-modal>Add Fortune</button>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Fortune</th>
              <th scope="col">Author</th>
              <th scope="col">Approved?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(fortune, index) in fortunes" :key="index">
              <td>{{fortune.fortune}}</td>
              <td>{{fortune.author}}</td>
              <td>
                <span v-if="fortune.approved">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <button type="button" class="btn btn-info btn-sm" @click="onApproveFortune(fortune)">Approve</button>
                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteFortune(fortune)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addFortuneModal" id="fortune-modal" title="Add a fortune" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-edit-group" label="Title:" label-for="form-title-edit-input">
          <b-form-input
            id="form-title-edit-input"
            type="text"
            v-model="addFortuneForm.title"
            required
            placeholder="Enter Title"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="form-author-edit-group"
          label="Author:"
          label-for="form-author-edit-input"
        >
          <b-form-input
            id="form-author-edit-input"
            type="text"
            v-model="addFortuneForm.author"
            required
            placeholder="Enter Author"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-approve-edit-group">
          <b-form-checkbox-group v-model="addFortuneForm.approved" id="form-checks">
            <b-form-checkbox value="false">Approved?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Fortune',
  data () {
    return {
      fortunes: [],
      addFortuneForm: {
        id: '',
        title: '',
        author: '',
        approved: []
      },
      message: '',
      showMessage: false
    }
  },
  methods: {
    getFortunes () {
      this.$log.debug('Getting Fortunes')
      const path = 'http://localhost:8081/fortune/all'
      this.$log.debug('Getting Fortune from path: ', path)
      this.$log.debug('Calling GET fortune/all')
      axios
        .get(path)
        .then(res => {
          this.fortunes = res.data
          this.$log.debug('Response Payload: ', res.data)
        })
        .catch(error => {
          this.$log.error(error)
        })
    },
    addFortune (payload) {
      this.$log.debug('Adding new fortune')
      const path = 'http://localhost:8081/fortune'
      this.$log.debug('Posting to: ', path)
      this.$log.debug('Calling POST /fortune with payload: ', payload)
      axios.post(path, payload)
        .then(() => {
          this.$log.debug('Updating fortunes')
          this.getFortunes()
        })
        .catch((error) => {
          this.$log.error(error)
        })
    },
    onApproveFortune (fortune) {
      this.$log.debug('Clicked Approved button')
      this.approveFortune(fortune.id)
    },
    approveFortune (fortuneID) {
      this.$log.debug('Approving fortune')
      const path = `http://localhost:8081/fortune/${fortuneID}`
      this.$log.debug('Posting to: ', path)
      this.$log.debug('Calling PUT /fortune/{id}: ')
      axios.put(path)
        .then(() => {
          this.$log.debug('Updating fortunes')
          this.getFortunes()
        })
        .catch((error) => {
          this.$log.error(error)
        })
    },
    initForm () {
      this.$log.debug('Creating init form')
      this.addFortuneForm.title = ''
      this.addFortuneForm.author = ''
      this.addFortuneForm.read = []
    },
    onSubmit (evt) {
      this.$log.debug('Submitting Add Fortune form')
      evt.preventDefault()
      this.$refs.addFortuneModal.hide()
      const payload = {
        title: this.addFortuneForm.title,
        author: this.addFortuneForm.author
      }
      this.addFortune(payload)
      this.initForm()
    },
    onReset (evt) {
      evt.preventDefault()
      this.$refs.addFortuneModal.hide()
      this.initForm()
    },
    removeFortune (fortuneID) {
      this.$log.debug('Adding new fortune')
      const path = `http://localhost:8081/fortune/${fortuneID}`
      this.$log.debug('Calling url: ', path)
      this.$log.debug('Calling DELETE /fortune/{id}')
      axios.post(path)
        .then(() => {
          this.$log.debug('Delete Fortune!')
          this.message = 'Fortune Removed!'
          this.showMessage = true
          this.$log.debug('Updating fortunes')
          this.getFortunes()
        })
        .catch((error) => {
          this.$log.error(error)
          this.getFortunes()
        })
    },
    onDeleteFortune (fortune) {
      this.$log.debug('Calling Delete Fortune')
      this.removeFortune(fortune.id)
    }
  },
  created () {
    this.$log.debug('Fortune Component Created')
    this.getFortunes()
  }
}
</script>

<style scoped>
h1 img {
  display: inline;
}
th:nth-child(1) {
  width: 50%;
}
th:nth-child(2),
th:nth-child(4) {
  width: 20%;
}
th:nth-child(3) {
  width: 10%;
}
#add-fortune-button {
  margin: 1em;
}
</style>
