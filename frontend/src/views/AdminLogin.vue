<template>
    <h1>GAIN ADMIN RIGHTS</h1>
    <form>
        <input
            id="password"
            v-model="form.password"
            placeholder="password"
        />
        <pre>{{ JSON.stringify(response, null, 2) }}</pre>
        <div>{{ massage }}</div>
    </form>
</template>

<script>
</script>