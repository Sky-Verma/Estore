var bar = document.querySelector('.fa-bars');
var times = document.querySelector('.fa-times');
var tl_show = new TimelineLite({ paused: true });
tl_show.to('.fa-bars',
{
    display: 'none',
    duration: 0.5
}).to('.fa-times',{
display:'block'
});
bar.addEventListener('click', () => {
    tl_show.play();
    document.querySelector('.nav-list').className = 'nav-list-show';
});
times.addEventListener('click', () => {
    tl_show.reverse();
    document.querySelector('.nav-list-show').className = 'nav-list';
});
window.onresize = () => {
    if (window.innerWidth > 540) {
        bar.style.display = 'none';
        times.style.display = 'none';
        document.querySelector('.nav-list').style.display = 'flex';
    } else {
        if (bar.style.display == 'block') {
            times.style.display = 'none';
            document.querySelector('.nav-list').style.display = 'none';
            bar.addEventListener('click', () => {
                tl_show.play();
                document.querySelector('.nav-list').className = 'nav-list-show';
            });
            times.addEventListener('click', () => {
                tl_show.reverse();
            });
        }
        else {
            bar.style.display = 'block';
            document.querySelector('.nav-list').style.display = 'none';
            bar.addEventListener('click', () => {
                tl_show.play();
            });
            times.addEventListener('click', () => {
                tl_show.reverse();
                document.querySelector('.nav-list-show').className = 'nav-list';
            });

        }
    }
};




