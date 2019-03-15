<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>
            <img src="../assets/fortune-cookie.png" alt="fortune cookie" height="42" width="42">
            Fortunes
        </h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Fortune</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Fortune</th>
              <th scope="col">Author</th>
              <th scope="col">Reviewed?</th>
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

<style scoped>
h1 img {
  display:inline;
}
th:nth-child(1){
   width: 50%;
}
th:nth-child(2), th:nth-child(2){
   width: 20%;
}
th:nth-child(3){
   width: 10%;
}
</style>