<template>
  <div class="page-header">
    <router-link to="/" class="back-button">← BACK</router-link>
    <div class="layout">
        <div class="page-signal">
          <span class="header-text">PICK A POLL</span>
          <span class="header-text2">TO VOTE</span>
        </div>  
        <p1 class="info-text">Pick an active poll or look through previous ones</p1>
        <router-link to="/voting" class="poll-box">
            <div class="title">
                <span class="poll-title">DECEMBER</span> 
                <span class="poll-status">VOTE</span>
            </div>
            <p class="text">DATE - DATE</p>
        </router-link>
    </div>
</div>   
</template>


<style>
.text{
color: gray;
font-size: 12px;
position: center;
}
.back-button {
  padding-bottom: 30px;
  color:#0f6f62;
}

.page-header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-top: 2cap;
}
.poll-title {
  color: rgba(149, 91, 153, 1);
}

.poll-status {
  color: rgb(0, 0, 0);
  padding-bottom: 1cap;
}
.title {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.layout {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
}

span {
  display: inline-block;
  padding: 5px;
}

.poll-box {
    display: flex;
    flex-direction: column;
    background-color: azure;
    padding: 1rem;
}

.header-text {
    color:rgba(244, 233, 172, 1) ;
    inset-inline: auto;
    font-size: 23px
}

.header-text2 {
    color:rgba(149, 91, 153, 1);
    inset-inline: auto;
    font-size: 24px
}

.info-text {
    color:rgba(244, 233, 172, 1) ;
    text-align: center;
    
}

.page-signal{
  margin: auto;
}
</style>