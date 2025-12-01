<template>
    <div class="container">
        <p class="header-block">
            <p>DATE</p>
            <p>CAT</p>
        </p>
        <div class="event-block">
           <div class="event-contents"> 
                <h1>TITLISSE</h1>
                <p>descritpion
                    adsasdadsdddddddddd
                    sdfsdfsdfsdfvs s s s s s s  s s s s 
                    sdfsdfsdfsdfsdfsssssssssssssssssss
                 fsdfsdf
                </p>
            </div>
            <div class="more-button">more burron</div>
        </div>
    </div>
</template>

<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
}

.container{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100vw;
    margin-left: 0;
    position: absolute;
    left: 0;

}

.header-block{
    background: rgba(6, 95, 83, 1);
    color:black;
    left: 0px;
    height: 10.5rem;
    inline-size: 25%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: right;
    font-size: 23px;
    color: rgba(244, 233, 172, 1);
    
}

.event-block{
    background: white;
    inline-size: 72.5%;
    display: flex;
    flex-direction: column;
    overflow-wrap: break-word;

}

.event-contents{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 6%;
    color: black
}

.more-button{
    position: absolute;
    bottom: 0;
    right: auto;
    left: auto;
    width: 72.5%;
    border-color: rgba(149, 91, 153, 1);
    border-width: 3.5px;
    background-color: aliceblue;
    color: rgba(149, 91, 153, 1);
    border-style: solid;
    text-align: center;
    height: 2rem;
}

h1{
    font-size: 23px
}


</style>