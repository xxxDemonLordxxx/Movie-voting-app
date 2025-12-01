<template>
  <div class="page-header">
      <router-link to="/" class="back-button">← BACK</router-link>
      <div class="title">
        <span class="poll-title">DECEMBER</span> 
        <span class="page-title">POLL</span>
      </div>
    </div>
    
    <form>
      <div class="input-group">
        <p class="number">1</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
      </div>

      <div class="input-group">
        <p class="number">2</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
      </div>

      <div class="input-group">
        <p class="number">3</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
      </div>

      <div class="input-group">
        <p class="number">4</p>
        <textarea
          id="movieDescription"
          placeholder="Search"
          required
          rows="1"
          class="form-textarea"
        ></textarea>
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
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 10px;
  border: 2.5px solid gray;
  font-size: 16px;
}

.number {
  color: black;
  padding: 5px;
}
</style>