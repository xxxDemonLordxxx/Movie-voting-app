<template>
  <div class="page-header">
      <router-link to="/polls" class="back-button">← BACK</router-link>
      <div class="title">
        <span class="poll-title">DECEMBER</span> 
        <span class="page-title">POLL</span>
      </div>
    </div>
    
    <form>
      <div class="input-group">
        <p class="number">1</p>
        <p class="search-pretty">(</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
        <p class="search-pretty">)</p>
      </div>

      <div class="input-group">
        <p class="number">2</p>
        <p class="search-pretty">(</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
        <p class="search-pretty">)</p>
      </div>

      <div class="input-group">
        <p class="number">3</p>
        <p class="search-pretty">(</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
        <p class="search-pretty">)</p>
      </div>

      <div class="input-group">
        <p class="number">4</p>
        <p class="search-pretty">(</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
        <p class="search-pretty">)</p>
      </div>

    </form>
    

</template>

<style>

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
}


.text{
color: white;
font-size: 16px;
position: center;
}

.back-button {
  padding-bottom: 30px;
  color:#0f6f62;
}

.page-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding-top: 2cap;
}
.poll-title {
  color: rgba(149, 91, 153, 1);
}

.page-title {
  color: aliceblue;
  padding-bottom: 1cap;
}
.title {
  inset-inline: auto;
  
}

span {
  display: inline-block;
  padding: 5px;
}

.input-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background-color: white;
  align-items: center;
  line-height: 1.2
}

.form-input,
.form-textarea {
  width: 100%;
  border: 0;
  font-size: 16px;
  font-weight: 600;
  color: rgb(82, 39, 85);
}

.number {
  color: black;
  padding: 0.3rem;
}

.search-pretty {
  color: rgba(149, 91, 153, 1);
  font-size: 1.50rem;
  font-weight: 350;
  font-family:Verdana, Geneva, Tahoma, sans-serif;
  padding-left: 0.3rem;
  padding-right: 0.3rem;
}
</style>