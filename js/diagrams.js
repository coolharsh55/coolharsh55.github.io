// Render GraphViz/DOT diagrams on the page
// Diagrams are in <pre><code> elements with class 'renderDiagram'
// The script will render the diagram and replace the code with an image
var diagram_codes = document.getElementsByClassName('renderDiagram');
for (const index in diagram_codes) {
    let code = diagram_codes[index];
    var viz = new Viz();
    viz.renderImageElement(code.textContent)
        .then(function(element) {
            code.parentNode.insertBefore(element, code);
            code.style.display = 'none';
        }).catch(error => {
            // Create a new Viz instance (@see Caveats page for more info)
            viz = new Viz();
            // Possibly display the error
            console.error(error);
        });
    }   