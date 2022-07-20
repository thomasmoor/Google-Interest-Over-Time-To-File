<div>
  <div id="myDiv">
  
    <label htmlFor='prompt'>Keywords (up to 5, separated by commas):</label>
    <input type='text' required id='keywords' />
		
    <button onclick="exec()">Google Trends</button>
    <br/>
		
  </div>
</div>

<script type='text/javascript'>
  // create an element
  const createNode = (elem) => {
    return document.createElement(elem);
  };

  // append an element to parent
  const appendNode = (parent, elem) => {
    parent.appendChild(elem);
  }
  
  function exec(){
    
    console.log("this.keywords: "+this.keywords.value)
    
    const api = 'https://thomasmoor.org/getgoogleiot';

    // post body data
    const enteredData = {
      keywords: this.keywords.value,
    };
    
    // create request object
    const request = new Request(api, {
      method: 'POST',
      body: JSON.stringify(enteredData),
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    });
    
	const body = document.body,
          tbl = document.createElement('table');
    tbl.style.width = '100%';
    tbl.style.border = '1px solid black';
    
    // Headers
	var tr = tbl.insertRow();
    var td = tr.insertCell();
    td.style.border = '1px solid black';
	td.appendChild(document.createTextNode('Keyword'));
    td = tr.insertCell();
    td.style.border = '1px solid black';
	td.appendChild(document.createTextNode('Last'));
    td = tr.insertCell();
    td.style.border = '1px solid black';
	td.appendChild(document.createTextNode('Max'));
    td = tr.insertCell();
    td.style.border = '1px solid black';
	td.appendChild(document.createTextNode('Min'));
    td = tr.insertCell();
    td.style.border = '1px solid black';
	td.appendChild(document.createTextNode('Avg 5Y'));
    td = tr.insertCell();
    td.style.border = '1px solid black';
	td.appendChild(document.createTextNode('Avg 1Y'));
    td = tr.insertCell();
    td.style.border = '1px solid black';
	td.appendChild(document.createTextNode('Avg 6M'));
	
    // pass request object to `fetch()`
    fetch(request)
      .then(res => res.json())
      .then(res => {
        console.log("From API");
        console.log(res);
		
		res.map((row) => {
          console.log("row: "+row.keyword);
		  tr = tbl.insertRow();
          td = tr.insertCell();
          td.style.border = '1px solid black';
		  td.appendChild(document.createTextNode(row.keyword));	
          td = tr.insertCell();
          td.style.border = '1px solid black';
		  td.appendChild(document.createTextNode(row.last));
          td = tr.insertCell();
          td.style.border = '1px solid black';
		  td.appendChild(document.createTextNode(row.max));
          td = tr.insertCell();
          td.style.border = '1px solid black';
		  td.appendChild(document.createTextNode(row.min));
          td = tr.insertCell();
          td.style.border = '1px solid black';
		  td.appendChild(document.createTextNode(row.mal));
          td = tr.insertCell();
          td.style.border = '1px solid black';
		  td.appendChild(document.createTextNode(row.mam));
          td = tr.insertCell();
          td.style.border = '1px solid black';
		  td.appendChild(document.createTextNode(row.mas));
		});
		
        console.log("Done.");
    }).catch(err => {
        console.error('Error: ', err);
    });

    document.getElementById("myDiv").appendChild(tbl);
  } // exec()
  
  async function saveAsFile() {
      console.log("saveAsFile")
      var prefix = ""; // document.getElementById("category").value;
      var textToSave = "GPT-3\n";
	  textToSave+=document.getElementById("GPT3").value;
	  textToSave+="\nGPT-Neo\n";
	  textToSave+=document.getElementById("GPTNeo").value;
      console.log("t: "+textToSave)

      var fileNameToSaveAs = "thomasmoor.org.txt";
 
      var textToSaveAsBlob = new Blob([textToSave], {type:"text/plain"});
      var textToSaveAsURL = window.URL.createObjectURL(textToSaveAsBlob);

      var downloadLink = document.createElement("a");
      downloadLink.download = fileNameToSaveAs;
      downloadLink.innerHTML = "Download File";
      downloadLink.href = textToSaveAsURL;
      downloadLink.onclick = destroyClickedElement;
      downloadLink.style.display = "none";
      document.body.appendChild(downloadLink);
 
      downloadLink.click();
  } // saveTextAsFile
  
  async function destroyClickedElement(event){
    document.body.removeChild(event.target);
  }
  
</script>