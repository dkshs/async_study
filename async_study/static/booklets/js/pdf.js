function createPDFContainer(url) {
  const container = document.getElementById("booklet_pdf");

  pdfjsLib.getDocument(url).promise.then((pdf) => {
    pdf.getPage(1).then((page) => {
      const canvas = document.createElement("canvas");
      const context = canvas.getContext("2d");
      const viewport = page.getViewport({ scale: 1.5 });

      canvas.width = viewport.width;
      canvas.height = viewport.height;

      page.render({ canvasContext: context, viewport }).promise.then(() => {
        container.appendChild(canvas);
      });
    });
  });
}
