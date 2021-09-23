import originAxios from 'axios';
import { LOCAL_HOST, PORT_NUM } from "../utils/constant";

export default function request(option) {

  return new Promise((resolve, reject) => {
    // New Axios

    const instance = originAxios.create({
      baseURL: `http://${LOCAL_HOST}:${PORT_NUM}/`,
      timeout: 150000
    });
    // configure request para
    instance.interceptors.request.use(config => {
      return config;
    }, err => {
      return err;
    });

    instance.interceptors.response.use(response => {
      return response.data;
    }, err => {
      if (err && err.response) {
        switch (err.response.status) {
          case 400:
            err.message = 'Request Failure';
            break;
          case 401:
            err.message = 'Not Authorized';
            break;
          case 403:
            err.message = 'Wrong user infomation';
            break;
          case 404:
            err.message = 'not found';
            break;
          default:
            err.message = "Other Mistake";
        }
      }
      return Promise.reject(err);
    });

    //make request with new parameters
    instance.request(option).then(res => {
      resolve(res);
    }).catch(err => {
      reject(err);
    });
  });
}
