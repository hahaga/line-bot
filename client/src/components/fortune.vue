<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>
            <img src="../assets/fortune-cookie.png" style="display:inline;" alt="fortune cookie" height="42" width="42">
            Fortunes
        </h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Fortune</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" style="width: 50%">Fortune</th>
              <th scope="col" style="width: 20%">Author</th>
              <th scope="col" style="width: 10%">Reviewed?</th>
              <th style="width: 20%"></th>
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
                <button type="button" class="btn btn-info btn-sm">Edit</button>
                <button type="button" class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Fortune',
  data(){
    return {
      fortunes: [],
    };
  },
  methods: {
    getFortunes(){
      const path="http://localhost:8081/fortune";
      axios.get(path)
        .then((res) => {
          this.fortunes = res.data.fortunes;
        })
        .catch((error) => {
          console.log(error);
        });
    },      
  },
  created(){
    this.getFortunes();
  }
};
</script>
