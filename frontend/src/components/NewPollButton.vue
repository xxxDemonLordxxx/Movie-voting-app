<template>
    <dialog ref="dialogRef">
        <form @submit.prevent="handleSubmit">
            <button 
                type="button" 
                aria-label="close"
                @click="closeDialog"
                formnovalidate>X
            </button>
            <h2 id="CreatePollid">Create new poll</h2>
            <input
                id="pollTitle"
                v-model="form.pollTitle"
                placeholder="Write the title of the poll"
                class="form-input"
                required
            />
            <button type="submit">Submit</button>
        </form>
    </dialog>
    <p>
        <button @click="showDialog">New poll</button>
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
        handleSubmit() {
            this.closeDialog();
        },

        
        async submitPoll() {
          
          this.submitting = true
        
          try {
          const response = await fetch('http://localhost:8000/polls/new', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              title: this.form.pollTitle,
            })
          })

          if (response.ok) {
            alert('Poll Submitted')
            this.resetForm()
            this.$router.push('/')
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