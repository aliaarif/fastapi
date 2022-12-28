<template>
    <div id="dashboard-wrapper" class="dashboard-outer" x-data="initBlank()" :class="{
        'is-pushed': $store.app.sidebarOpenedState,
        '': !$store.app.sidebarOpenedState
    }">
        <div class="dashboard-inner">

            <div class="dashboard-wrapper">
                <div id="main-dashboard" class="section-wrapper">

                    <div class="dashboard-columns">
                        <div class="columns is-multiline">
                            33333333333333333333333333333333333333333333333333333333333333333 Landing Page
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'LandingPage'
}
</script>