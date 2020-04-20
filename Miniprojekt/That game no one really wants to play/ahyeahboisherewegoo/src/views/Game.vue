<template>
    <div class="d-flex justify-center mt-2">
        <v-progress-linear
        v-for="i in bars"
        :key="i"
        :color="i.color" 
        :value="i.value" 
        height="20">
        {{i.name}}
        </v-progress-linear>
    </div>
</template>

<script>
export default {
    data: () => ({
        bars: [
            {name:"fear", color: "red", value:10},
            {name:"popularity", color: "blue", value:50},
            {name:"progress", color: "yellow", value:50}
        ]
    })
}
</script>