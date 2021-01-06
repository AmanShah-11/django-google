import React, { Component } from "react";
    import {
      Button,
      Modal,
      ModalHeader,
      ModalBody,
      ModalFooter,
      Form,
      FormGroup,
      Input,
      Label
    } from "reactstrap";

    export default class CustomModal extends Component {
      constructor(props) {
        super(props);
        this.state = {
          activeItem: this.props.activeItem
        };
      }
      handleChange = e => {
        let { name, value } = e.target;
        if (e.target.type === "checkbox") {
          value = e.target.checked;
        }
        const activeItem = { ...this.state.activeItem, [name]: value };
        this.setState({ activeItem });
      };
      render() {
        const { toggle, onSave } = this.props;
        return (
          <Modal isOpen={true} toggle={toggle}>
            <ModalHeader toggle={toggle}> Todo Item </ModalHeader>
            <ModalBody>
              <Form>
                <FormGroup>
                  <Label for="time_start">Start Time</Label>
                  <Input
                    type="text"
                    name="time_start"
                    value={this.state.activeItem.time_start}
                    onChange={this.handleChange}
                    placeholder="Enter Start Time"
                  />
                </FormGroup>
                <FormGroup>
                  <Label for="time_end">End Time</Label>
                  <Input
                    type="text"
                    name="end_time"
                    value={this.state.activeItem.time_end}
                    onChange={this.handleChange}
                    placeholder="Enter End Time"
                  />
                </FormGroup>
                <FormGroup>
                  <Label for="date">Date</Label>
                  <Input
                    type="text"
                    name="date"
                    value={this.state.activeItem.time_start}
                    onChange={this.handleChange}
                    placeholder="Enter Date"
                  />
                </FormGroup>
                <FormGroup>
                  <Label for="acitvity">Activity</Label>
                  <Input
                    type="text"
                    name="activity"
                    value={this.state.activeItem.time_end}
                    onChange={this.handleChange}
                    placeholder="Enter Activity"
                  />
                </FormGroup>
              </Form>
            </ModalBody>
            <ModalFooter>
              <Button color="success" onClick={() => onSave(this.state.activeItem)}>
                Save
              </Button>
            </ModalFooter>
          </Modal>
        );
      }
    }