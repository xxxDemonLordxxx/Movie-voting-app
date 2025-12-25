<template>
    <div class="event-container">
        <div class="header-block">
            <p>31/06 17:20</p>
            <p>MAIN CAMPUS</p>
        </div>
        <div class="event-block">
            <h3 class="event-title">LONG ASSASASASSASSASS TITLISSE</h3>
            <p class="description">desc riD ED DE D A SSSD ASD ASD Asd ASSDSD SSSSSS SSSS SSSSSSSS SSS SSSS tpio fsdfsdf</p>

        </div>
        <div class="event-block">
            <img src='@/assets/more_button.png' @click="viewSubmission(submission.id)" class="more-button" />
        </div>
    </div>

</template>

<style>

.event-container{
    display: flex;
    flex-direction: row;
    box-sizing:border-box;
    height: 10rem;
    width: 100vw;
    margin-left: -50vw;
    position: relative;
    left: 50%;
    gap: 0.5rem;
}

.header-block{
    background: rgb(78, 32, 82);
    color:black;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: right;
    font-size: 13spx;
    color: white;
    border-color: rgb(199, 107, 208);;
    border-width: 0rem;
    border-style: dotted;

}

.event-block{

    display: flex;
    flex-direction: row;
    color: white;
    border-color: gray;
    border-width: 0.1rem;
    border-style: dotted;
    

}

.more-button{
    color: #023730;
    text-align: center;
    font-size: 1rem;
    writing-mode: vertical-rl;
    text-orientation: upright;
    margin: 0.2rem;
    padding: 0;
    background-color: #02373000;
    border: none;
}

h1{
    font-size: 23px;
}

.description{
    overflow-wrap: break-word;
    overflow:hidden;
    padding-left: 0.5rem;
    text-overflow: ellipsis;
    font-size: 0.72rem;
}

.event-title {
    font-family: "Blackout Two AM";
    overflow-wrap: break-word;
    flex-grow: 2;
    text-overflow: ellipsis;
    overflow:hidden

}

@media (min-width: 784px) {
    .event-container {
        right:50%;
        margin-left:-31rem;
    }
    .header-block{
        padding-left: 5rem;
    }
}

    
</style>