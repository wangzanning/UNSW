import {notification} from "antd";

export const showSuccessMessage = (message) => {
  notification.open({
    message: 'SUCCEED!',
    description: message,
    duration: 3,
    onClick: () => {
      console.log('GOOD!');
    }
  });
};

export const showFailuerMessage = (message) => {
  notification.open({
    message: 'FAILURE!',
    description: message,
    duration: 5,
    onClick: () => {
      console.log('Failed');
    }
  });
};

export const showLoadingMessage = (message) => {
  notification.open({
    message: 'UPLOADING!',
    description: message,
    duration: 5,
    onClick: () => {
      console.log('Uploading');
    }
  });
};
