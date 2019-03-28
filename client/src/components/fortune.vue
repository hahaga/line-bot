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
        <b-form-group id="form-fortune-edit-group" label="Fortune:" label-for="form-fortune-edit-input">
          <b-form-input
            id="form-fortune-edit-input"
            type="text"
            v-model="addFortuneForm.fortune"
            required
            placeholder="Enter Fortune"
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
        fortune: '',
        author: '',
        approved: []
      },
      message: '',
      showMessage: false
    }
  },
  methods: {
    getFortunes () {
      const path = 'https://uz1hyfe7ah.execute-api.us-west-2.amazonaws.com/dev/fortune/all'
      axios
        .get(path)
        .then(res => {
          this.fortunes = res.data
          this.$log.debug('Response Payload: ', res.data)
        })
        .catch(error => {
          this.$log.debug('In getFortunes(), path: ', path, '  error: ', error)
        })
    },
    addFortune (payload) {
      const path = 'https://uz1hyfe7ah.execute-api.us-west-2.amazonaws.com/dev/fortune'
      axios.post(path, payload)
        .then(() => {
          this.getFortunes()
        })
        .catch((error) => {
          this.$log.debug('In addFortune(), path: ', path, '  error: ', error)
          this.$log.debug('Payload was: ', payload)
        })
    },
    onApproveFortune (fortune) {
      this.approveFortune(fortune.id)
    },
    approveFortune (fortuneID) {
      const path = `https://uz1hyfe7ah.execute-api.us-west-2.amazonaws.com/dev/fortune/${fortuneID}`
      axios.put(path)
        .then(() => {
          this.getFortunes()
        })
        .catch((error) => {
          this.$log.debug('In approveFortune(), path: ', path, '  error: ', error)
        })
    },
    initForm () {
      this.addFortuneForm.fortune = ''
      this.addFortuneForm.author = ''
      this.addFortuneForm.read = []
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addFortuneModal.hide()
      const payload = {
        fortune: this.addFortuneForm.fortune,
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
      const path = `https://uz1hyfe7ah.execute-api.us-west-2.amazonaws.com/dev/fortune/${fortuneID}`
      axios.delete(path)
        .then(() => {
          this.message = 'Fortune Removed!'
          this.showMessage = true
          this.getFortunes()
        })
        .catch((error) => {
          this.$log.debug('In removeFortune(), path: ', path, '  error: ', error)
          this.getFortunes()
        })
    },
    onDeleteFortune (fortune) {
      this.removeFortune(fortune.id)
    }
  },
  created () {
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
