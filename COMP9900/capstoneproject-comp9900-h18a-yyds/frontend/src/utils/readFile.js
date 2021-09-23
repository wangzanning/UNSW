
export function readFile (event) {
  const reader = new FileReader();
  reader.readAsDataURL(event.fileList[0]);
  return reader.onloadend = () => reader.result;
}

export const normFile = (e) => {

  if (Array.isArray(e)) {
    return e;
  }

  return e && e.fileList;
};
