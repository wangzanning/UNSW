import React, { useLayoutEffect, useState } from 'react';
import { useHistory } from "react-router-dom";
import { InboxOutlined, PlusOutlined, UploadOutlined } from '@ant-design/icons';
import { postRecipeRequest, getCategoryRequest } from "../../services/postRecipe";
import 'antd/dist/antd.css';
import './index.css';
import { showSuccessMessage, showFailuerMessage, showLoadingMessage } from "../../utils/popMessage";
import { Form, Input, Button, Select, Upload, Space, PageHeader, BackTop, Progress, Spin } from 'antd';
import { shallowEqual, useSelector } from "react-redux";
import { normFile } from "../../utils/readFile";

const { Option } = Select;
const layout = {
  labelCol: {
    span: 8
  },
  wrapperCol: {
    span: 16
  }
};
const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16
  }
};

export default function PostDishes() {
  const [loadingState, setLoadingState] = useState(false);
  const history = useHistory();
  const [percent, setPercent] = useState(0);
  const [allFileList, setAllFileList] = useState([]);
  const [allMethodList, setAllMethodList] = useState({});
  const [allCategory, setAllCategory] = useState([]);
  const { token } = useSelector(state => ({
    token: state.login.get("token")
  }), shallowEqual);
  const [form] = Form.useForm();
  let methodCounter = 0;

  useLayoutEffect(() => {
    getCategoryRequest().then((res) => {
      setAllCategory(res.types);
    });
  }, []);
  const submitNewRecipe = (value) => {
    // console.log(titleRef.current.value);
    if (allFileList.length === 0) {
      showFailuerMessage('the photo should not be empty');
      return;
    }
    setLoadingState(true);
    showLoadingMessage('Your recipe is being uploaded');
    let resFileList = allFileList.map((item) => item.base64);
    value.image = resFileList[0];
    // console.log(value);
    let tempPhotoList = [];
    for (let i in allMethodList) {
      tempPhotoList.push(allMethodList[i]);
    }
    for (let i = 0; i < value.methods.length; i++) {
      value.methods[i]['thumbnail'] = tempPhotoList[i];
    }
    delete value.Photoes;
    postRecipeRequest(value, token).then((res) => {
      if (res) {
        showSuccessMessage('Go to your main page, and check your new post!');
        setLoadingState(false);
        form.resetFields();
        history.push('./feed');
      } else {
        showFailuerMessage('Something wrong, try again later');
        setLoadingState(false);
      }
    });
  };
  const onReset = () => {
    form.resetFields();
  };

  //handle photos in Photos
  const handleUploadImage = (event) => {
    let fileList = [...event.fileList];
    fileList.forEach(function (file) {
      let reader = new FileReader();
      reader.onload = (e) => {
        file.base64 = e.target.result;
      };
      reader.readAsDataURL(file.originFileObj);
    });
    setAllFileList(fileList);
  };

  //handle photo in methods
  const handleMethodPhotoes = async (event) => {
    let fileList = [...event.fileList];
    await fileList.forEach(function (file) {
      let reader = new FileReader();
      reader.onload = (e) => {
        file.base64 = e.target.result;
        allMethodList[methodCounter] = e.target.result;
        setAllMethodList(allMethodList);
      };
      reader.readAsDataURL(file.originFileObj);
    });
  };

  const percentIncrease = () => {
    let cur_percent = percent + 10;
    if (cur_percent > 100) {
      cur_percent = 100;
    }
    setPercent(cur_percent);
  };

  const percentIncreaseFinish = () => {
    let cur_percent = percent + 50;
    if (cur_percent > 100) {
      cur_percent = 100;
    }
    setPercent(cur_percent);
  };

  return (
    <div className="container">
      <PageHeader
        className="site-page-header"
        onBack={() => history.push('/feed')}
        title="NEW RECIPE"
        subTitle="Create your New recipe on this page"
      />,
      <Spin spinning={loadingState} size="large" tip="Uploading">
        <Form {...layout} style={{ width: '55%' }} form={form} name="post-recipe" onFinish={submitNewRecipe}>
          {/*fill title, type*/}
          <Progress percent={percent} className="progressClass" strokeColor="rgba(218, 157, 66, 0.5)" />
          <Form.Item
            name="title"
            label="Title"
            rules={[{ required: true }]}
          >
            <Input className="input-box" onClick={percentIncrease} placeholder="Think of an awesome name for your recipe" />
          </Form.Item>
          <Form.Item
            name="abstract"
            label="Abstract"
            rules={[{ required: true }]}
          >
            <Input className="input-box" onClick={percentIncrease} placeholder="Briefly introduce your recipe" />
          </Form.Item>
          <Form.Item
            name="meal_type"
            label="Meal type"
            rules={[{ required: true }]}
          >
            <Select
              mode="multiple"
              placeholder="Select a type for your Recipe"
              allowClear
              className="input-box"
              onChange={percentIncrease}
            >
              {
                allCategory && allCategory.map((item, index) => (
                  <Option key={index} value={item}>{item}</Option>
                ))
              }
            </Select>
          </Form.Item>
          {/* fill recipe ingredients*/}
          <Form.Item>
            <div className="link-top" />
          </Form.Item>
          <Form.Item
            rules={[{ required: true }]}
            name="ingredients"
            label="Ingredients"
          >
            <Form.List
              name="ingredients"
              rules={[
                {
                  validator: async (_, names) => {
                    if (!names || names.length < 1) {
                      return Promise.reject(new Error('At least 1 ingredients'));
                    }
                  }
                }
              ]}
            >
              {(fields, { add }, { errors }) => (
                <>
                  {fields.map(({ key, name, fieldKey, ...restField }) => (
                    <Space key={key} style={{ display: 'flex', marginBottom: 4 }} align="baseline">
                      <Form.Item>
                        Ingredient {fieldKey + 1} :
                      </Form.Item>
                      <Form.Item
                        {...restField}
                        style={{ width: "300px" }}
                        name={[name, 'ingredient']}
                        fieldKey={[fieldKey, 'ingredient']}
                        rules={[{ required: true, message: 'Missing ingredient' }]}
                        onClick={percentIncrease}
                      >
                        <Input className="input-box" placeholder="ingredient" />
                      </Form.Item>
                      <Form.Item
                        {...restField}
                        style={{ width: "100px" }}
                        name={[name, 'volume']}
                        fieldKey={[fieldKey, 'volume']}
                        rules={[{ required: true, message: 'Missing volume' }]}
                      >
                        <Input className="input-box" placeholder="volume" />
                      </Form.Item>
                      <Form.Item
                        style={{ width: "100px" }}
                        {...restField}
                        name={[name, 'unit']}
                        fieldKey={[fieldKey, 'unit']}
                        rules={[{ required: true, message: 'Missing unit' }]}
                      >
                        <Input className="input-box" placeholder="unit" />
                      </Form.Item>
                      {/*<MinusCircleOutlined onClick={() => remove(name)}/>*/}
                    </Space>
                  ))}
                  <Form.Item>
                    <Button
                      type="primary"
                      onClick={() => add()}
                      style={{ width: '60%' }}
                      icon={<PlusOutlined />}
                      className="add-button"
                    >
                      Add ingredient
                    </Button>
                    <Form.ErrorList errors={errors} />
                  </Form.Item>
                </>
              )}
            </Form.List>
          </Form.Item>
          <Form.Item>
            <div className="link-top" />
          </Form.Item>
          {/*fill methods*/}
          <Form.Item name="methods" label="Methods" rules={[{ required: true }]}>
            <Form.List
              name="methods"
              rules={[
                {
                  validator: async (_, names) => {
                    if (!names || names.length < 1) {
                      return Promise.reject(new Error('At least 1 methods'));
                    }
                  }
                }
              ]}
            >
              {(fields, { add }, { errors }) => (
                <>
                  {fields.map(({ key, name, fieldKey, ...restField }) => (
                    methodCounter = key,
                    <Space key={key} style={{ display: 'flex', marginBottom: 4 }} align="baseline">
                      <Form.Item>
                        Step {fieldKey + 1} :
                      </Form.Item>
                      <Form.Item
                        {...restField}
                        style={{ width: "400px" }}
                        name={[name, 'method']}
                        fieldKey={[fieldKey, 'methods']}
                        rules={[{ required: true, message: 'Missßing methods' }]}
                        onClick={percentIncrease}
                      >
                        <Input className="input-box" placeholder="methods" />
                      </Form.Item>
                      <Form.Item
                        rules={[
                          {
                            validator: async (_, names) => {
                              if (!names || names.length !== 1) {
                                return Promise.reject(new Error('please upload one photoes'));
                              }
                            }
                          }
                        ]}
                      >
                        <Upload maxCount={1} onChange={handleMethodPhotoes}>
                          <Button className="input-box" icon={<UploadOutlined />}>Upload</Button>
                        </Upload>
                      </Form.Item>
                      {/*<MinusCircleOutlined onClick={() => remove(name)}/>*/}
                    </Space>
                  ))}
                  <Form.Item>
                    <Button
                      type="primary"
                      onClick={() => add()}
                      style={{ width: '60%' }}
                      icon={<PlusOutlined />}
                      className="add-button"
                    >
                      Add Method
                    </Button>
                    <Form.ErrorList errors={errors} />
                  </Form.Item>
                </>
              )}
            </Form.List>
          </Form.Item>
          <Form.Item>
            <div className="link-top" />
          </Form.Item>
          {/*fill photoes for current recipe*/}
          <Form.Item label="Photos" rules={[{ required: true }]} onClick={percentIncreaseFinish} >
            <Form.Item name="Photoes" valuePropName="fileList" getValueFromEvent={normFile} className="input-box">
              <Upload.Dragger maxCount={1} name="files" onChange={handleUploadImage}>
                <p>
                  <InboxOutlined />
                </p>
                <p className="ant-upload-text">Click or drag file to this area to upload</p>
                <p className="ant-upload-hint">Support for a single or bulk upload.</p>
              </Upload.Dragger>
            </Form.Item>
          </Form.Item>
          {/*submit and reset button*/}
          <Form.Item {...tailLayout}>
            <Button htmlType="submit" type="default" className="button-style-submit">
              Submit
            </Button>
            <Button htmlType="button" onClick={onReset} className="button-style-reset">
              Reset
            </Button>
          </Form.Item>
        </Form>
      </Spin>

      <BackTop />
    </div>

  );
}
