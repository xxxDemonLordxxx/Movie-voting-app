<template>
   <div class="container"> 
    <dialog ref="dialogRef">
          <form @submit.prevent="SubmitPoll">
              <button  
                  type="button" 
                  aria-label="close"
                  @click="closeDialog"
                  formnovalidate>X
              </button>
              <h2 class="text" id="CreatePollid">Create new poll</h2>
              <input
                  id="pollTitle"
                  v-model="form.pollTitle"
                  placeholder="Write the title of the poll"
                  class="form-input"
                  required
              />
              <input
                  type="datetime-local"
                  id="pollEnd"
                  name="meeting-time"
                  value="2018-06-12T19:30"
                />
              <button class="btn" @click="SubmitPoll">Submit</button>
          </form>
      </dialog>
    </div>
    <p>
        <button class="btn" @click="showDialog">New poll</button>
    </p>
</template>

<script>
export default {
    name: 'Polls',
    data() {
        return {
            polls: [],
            loading: false,
            error: null,
            form: {
                pollTitle: '',
                pollEnd: '',
            },
            dialogRef: null
        }
    },
    mounted() {
        // Get the dialog element reference
        this.dialogRef = this.$refs.dialogRef;
    },
    methods: {
        showDialog() {
            if (this.dialogRef) {
                this.dialogRef.showModal();
            }
        },
        closeDialog() {
            if (this.dialogRef) {
                this.dialogRef.close();
                this.form.pollTitle = ''; // Clear form on close
            }
        },

        async SubmitPoll() {
          
          this.submitting = true
        
          try {
          const response = await fetch('http://localhost:8000/polls/new', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              title: this.form.pollTitle,
              end: this.form.pollEnd,
              state_id: 0
            })
          })

          if (response.ok) {
            alert('Poll Submitted')
            this.$router.push('/polls')
          } else {
            throw new Error('SENDING ERROR')
          }
        } catch (error) {
          console.error('Error:', error)
          alert('SENDING ERROR при отправке предложения')
        } finally {
          this.submitting = false
        }
      },
    }
}
</script>

<style>
.btn {
  display: inline-block;
  padding: 6px 12px;
  background-color: rgba(244, 233, 172, 1);
  color: rgb(45, 35, 35);
  text-decoration: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  margin: 0.5rem;
}

.text{
  margin: 10px;
  font-size: 22px;
}

.dialog-box{
  display: block;
  margin: auto;
  width: 60vw;
}

.form-input{
  margin: 10px;
  width: 40vw;
  
}

.container{
  position: auto;
  max-width: 55vw
}
</style>