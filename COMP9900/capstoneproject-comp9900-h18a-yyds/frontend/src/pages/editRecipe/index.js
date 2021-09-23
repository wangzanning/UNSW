import React, { useEffect, useLayoutEffect, useState } from 'react';
import { useHistory, useLocation } from "react-router-dom";
import { InboxOutlined, PlusOutlined, UploadOutlined } from '@ant-design/icons';
import { editRecipeRequest, getCategoryRequest } from "../../services/editRecipe";
import 'antd/dist/antd.css';
import { Form, Input, Button, Select, Upload, Space, PageHeader, Image, BackTop, Spin } from 'antd';
import { shallowEqual, useSelector } from "react-redux";
import { getRecipeById } from "../../services/recipe";
import { normFile } from "../../utils/readFile";
import { showSuccessMessage, showFailuerMessage, showLoadingMessage } from "../../utils/popMessage";
import './index.css';

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

export default function EditRecipe() {
  const location = useLocation();
  const history = useHistory();
  const { token } = useSelector(state => ({
    token: state.login.get("token")
  }), shallowEqual);
  const [form] = Form.useForm();
  const formRef = React.useRef();
  const [loadingState, setLoadingState] = useState(false);
  const postId = location['pathname'].replace('/editRecipe/', '');
  const [title, setTitle] = useState("");
  const [abstract, setAbstract] = useState("");
  // eslint-disable-next-line no-unused-vars
  const [image, setImage] = useState("");
  const [oldPost, setOldPost] = useState([]);
  const [allCategory, setAllCategory] = useState([]);
  const [currentCate, setCurrentCate] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  let [allFileList, setAllFileList] = useState([]);
  const [oldMethod, setOldMethod] = useState([]);

  useEffect(
    () => {
      getRecipeById(postId).then((res) => {
        if (res) {
          setOldPost(res);
          setTitle(res.title);
          setAbstract(res.abstract);
          setImage(res.image);
          setCurrentCate(res.meal_type);
          setAllFileList(res.image);
          setIngredients(res.ingredients);
          setOldMethod(res.methods);
        }
      });
    }, []);
  //reset the form
  const onReset = () => {
    form.resetFields();
  };
  useLayoutEffect(() => {
    getCategoryRequest().then((res) => {
      setAllCategory(res.types);
    });
  }, []);

  //submit the edit post and send to the backend
  const submitEditPost = (res) => {
    setLoadingState(true);
    showLoadingMessage('Your recipe is being uploaded');
    if (res) {
      res.image = allFileList;
      delete res.Photoes;
      for (let i = 0; i < res.methods.length; i++) {
        res.methods[i].thumbnail = oldMethod[i].thumbnail;
      }
      res.author_id = oldPost.author_id;
      res.last_modified = oldPost.last_modified;
      res.liked_num = oldPost.liked_num;
      res.rate_sum = oldPost.rate_sum;
      res.rate_by = oldPost.rate_by;
      res.comments_pages = oldPost.comments_pages;
      editRecipeRequest(res, postId, token).then((res) => {
        if (res) {
          setLoadingState(false);
          showSuccessMessage('Go to your main page, and check the post you edit!');
          history.push('./feed');
        } else {
          setLoadingState(false);
          showFailuerMessage('Something wrong, try again later');
        }
      });
    }
  };

  //upload data image
  const handleUploadImage = async (event) => {
    let fileList = [...event.fileList];
    await fileList.forEach(function (file) {
      let reader = new FileReader();
      reader.onload = (e) => {
        file.base64 = e.target.result;
        setAllFileList(fileList[0].base64);
      };
      reader.readAsDataURL(file.originFileObj);
    });
  };

  //handle photo in methods
  const handleEditMethodPhotos = (event, key) => {
    let fileList = [...event.fileList];
    fileList.forEach(function (file) {
      let reader = new FileReader();
      reader.onload = (e) => {
        file.base64 = e.target.result;
        if (!oldMethod[key]) {
          oldMethod.push({});
        }
        oldMethod[key].thumbnail = e.target.result;
        setOldMethod(oldMethod);
      };
      reader.readAsDataURL(file.originFileObj);
    });
  };

  //load data before edit
  setTimeout(fillDefault, 500);

  //set the default value
  function fillDefault() {
    formRef.current.setFieldsValue({
      title: title,
      abstract: abstract,
      meal_type: currentCate,
      ingredients: ingredients,
      methods: oldMethod
    });
  }

  return (
    <div className="container">
      <PageHeader
        className="site-page-header"
        onBack={() => history.push('/feed')}
        title="EDIT RECIPE"
        subTitle="Edit your old recipe on this page"
      />
      <Spin spinning={loadingState} size="large" tip="Uploading">
        <Form {...layout} style={{ width: '55%' }} form={form} name="post-recipe" onFinish={submitEditPost} ref={formRef}>
          {/*fill title, type*/}
          <Form.Item
            name="title"
            label="Title"
            rules={[{ required: true }]}
          >
            <Input className="input-box" />
          </Form.Item>
          <Form.Item
            name="abstract"
            label="Abstract"
            rules={[{ required: true }]}
          >
            <Input className="input-box" />
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
            >
              {
                allCategory.map((item, index) => (
                  <Option key={index} value={item} class="select-options">{item}</Option>
                ))
              }
            </Select>
          </Form.Item>
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
                    </Space>
                  ))}
                  <Form.Item>
                    <Button
                      type="primary"
                      onClick={() => add()}
                      style={{ width: '60%' }}
                      className="add-button"
                      icon={<PlusOutlined />}
                    >
                      Add ingredients
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
          <Form.Item name="methods" label="Methods" rules={[{ required: true }]}>
            <Form.List
              className="borderline"
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
              {/* eslint-disable-next-line no-unused-vars */}
              {(fields, { add }, { errors }) => (
                <>
                  {fields.map(({ key, name, fieldKey, ...restField }) => (
                    <Space key={key} style={{ display: 'flex', marginBottom: 4 }} align="baseline" wrap>
                      <Form.Item>
                        Step {fieldKey + 1} :
                      </Form.Item>
                      <Form.Item
                        {...restField}
                        style={{ width: "400px" }}
                        name={[name, 'method']}
                        fieldKey={[fieldKey, 'methods']}
                        rules={[{ required: true, message: 'Missing methods' }]}
                      >
                        <Input className="input-box" placeholder="methods" />
                      </Form.Item>
                      <Form.Item
                        rules={[
                          {
                            validator: async (_, names) => {
                              if (!names || names.length !== 1) {
                                return Promise.reject(new Error('please upload one photo'));
                              }
                            }
                          }
                        ]}
                      >
                        <Upload maxCount={1} on onChange={(e) => handleEditMethodPhotos(e, key)}>
                          <Button className="input-box" icon={<UploadOutlined />}>Edit</Button>
                        </Upload>
                      </Form.Item>
                      {oldMethod[key] ?
                        <Image style={{ width: '200px', marginLeft: '20%' }} src={oldMethod[key].thumbnail} />
                        : null
                      }
                      {/* <MinusCircleOutlined onClick={() => remove(name)}/> */}
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
                    {/*<Form.ErrorList errors={errors}/>*/}
                  </Form.Item>
                </>
              )}
            </Form.List>
          </Form.Item>
          <Form.Item>
            <div className="link-top" />
          </Form.Item>
          <Form.Item label="Photos" rules={[{ required: true }]}>
            <Image
              width={'250px'}
              src={allFileList}
            />
            <Form.Item name="Photoes" valuePropName="fileList" getValueFromEvent={normFile} className="file-dragger-input-box">
              <Upload.Dragger maxCount={1} name="files" onChange={handleUploadImage} className="file-dragger">
                <InboxOutlined />
                <p className="ant-upload-text">Click or drag file to this area to edit current photo</p>
                <p className="ant-upload-hint">ONLY ACCEPT ONE PHOTO</p>
              </Upload.Dragger>
            </Form.Item>
          </Form.Item>

          {/*submit, reset and fill default button*/}
          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit" className="button-style-submit">
              Submit
            </Button>
            <Button htmlType="button" onClick={onReset} className="button-style-reset">
              Reset
            </Button>
            <Button htmlType="button" onClick={fillDefault} className="button-style-reset">
              Fill Default
            </Button>
          </Form.Item>
        </Form>
      </Spin>

      <BackTop />
    </div>
  );
}
