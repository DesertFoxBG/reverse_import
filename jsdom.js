var fs = require('fs');
const Store = require('data-store');
const styles_path = new Store({ path: 'styles.json' });
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
var divs_path = './divs.txt';
var classes_path = './classes.txt';

fs.readFile('./output.html', function read(err, data) {
    if(err) {
        return console.log(err);
    }
    
    content = data.toString();

    const dom = new JSDOM(content);

    // Getting <div> tags
    var els = dom.window.document.querySelectorAll('*[style]');
    var holder = [];
    var class_holder = [];
    var style_holder = [];

    for(var count = 0; count < els.length; count++) {
        var el_styles = els[count].style._values;
        if(els[count].getAttribute('class') === null) {
            els[count].setAttribute('class', 'test' + count.toString());
        }
        var el_class = els[count].getAttribute('class');
        console.log(el_class);
        class_holder.push(el_class);
        console.log(el_styles);
        JSON.stringify(el_styles);
        style_holder[count] = [el_class, el_styles];

        styles_path.set('jsonObject', style_holder);

        var cont = els[count].outerHTML;
        holder[count] = cont;
        //console.log(cont);
        //console.log(count);
    }

    console.log(class_holder.length);
    console.log(holder.length);

    class_holder = class_holder.join('\n->\n');

    fs.writeFile(classes_path, class_holder, 'utf8', function(err) {
        if(err) {
            throw err;
        }
    
        console.log('Done');
    });
    
    //console.log(holder);
    holder = holder.join('\n->\n');
    console.log(holder);
    //console.log(style_holder);

    fs.writeFile(divs_path, holder, 'utf8', function(err) {
        if(err) {
            throw err;
        }
    
        console.log('Done');
    });
});