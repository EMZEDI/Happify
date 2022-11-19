<template>
    <div class="app">

        <ListPlaylistVue title = "To do List">
            <draggable :list="todos">
                <PlaylistItemVue v-for="todo in todos" :key="todo.id" :item="todo"></PlaylistItemVue>
            </draggable>
        
        </ListPlaylistVue>
    </div>
    <div class="app">
        <ListPlaylistVue title = "In progress ">
            <PlaylistItemVue v-for="todo in inProgress" :key="todo.id" :item="todo"></PlaylistItemVue>
        </ListPlaylistVue>
    </div>
    <div class="app">
        <ListPlaylistVue title = "done">
            <PlaylistItemVue v-for="todo in Completed" :key="todo.id" :item="todo"></PlaylistItemVue>
        </ListPlaylistVue>
    </div>
</template>

<script>
import ListPlaylistVue from './ListPlaylist.vue';
import PlaylistItemVue from './PlaylistItem.vue';
import draggable from 'vuedraggable'


export default{
    data() {
        return{
        todos: [
            {
                id: 1,
                todo: 'read a book',
            },
        ],
        inProgress: [
            {
                id: 1,
                todo: 'a',
            },
        ],
        Completed: [
            {
                id: 1,
                todo: 'read a book',
            },
        ],
    }
},
components : {
    ListPlaylistVue,
    PlaylistItemVue,
    draggable
    

}
}
</script>

<style>
.app{
    display:flex;
    justify-content: center;
    margin: 50px 0;
}
</style>