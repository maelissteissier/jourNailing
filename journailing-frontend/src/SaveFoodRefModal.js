import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import React, {Component} from 'react';
import {Form} from "react-bootstrap";
import "./SaveFoodRefModal.css"

class SaveFoodRefModal extends Component {
    constructor(props) {
        super(props);
        this.state={
            foodName:"",
            quantity:props.quantity,
            calories:props.calories
        }
        this.handleFoodNameChange = this.handleFoodNameChange.bind(this);
        this.handleQuantityChange = this.handleQuantityChange.bind(this);
        this.handleCaloriesChange = this.handleCaloriesChange.bind(this);
        this.onSaveFood = this.onSaveFood.bind(this);
    }

    static getDerivedStateFromProps(props, state){
        return {
            quantity:props.quantity,
            calories:props.calories
        }
    }


    handleFoodNameChange(e){
        this.setState({foodName: e.target.value});
    }

    handleQuantityChange(e){
        let originQuantity = isNaN(parseFloat(this.state.quantity)) ? 0 : parseFloat(this.state.quantity);
        this.setState({quantity: originQuantity});
    }

    handleCaloriesChange(e){
        let originCalories = isNaN(parseFloat(this.state.calories)) ? 0 : parseFloat(this.state.calories);
        this.setState({calories: originCalories});
    }

    async onSaveFood() {
        const data = {
            name: this.state.foodName,
            original_calory: this.state.calories,
            original_quantity: this.state.quantity
        };

        try {
            const response = await fetch('http://localhost:5000/foodrefs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Failed to create FoodRef');
            }

            const newFoodRef = await response.json();
            console.log('New FoodRef:', newFoodRef);
        } catch (error) {
            console.error('Error creating FoodRef:', error);
        }
    };

    render() {
        return (
            <Modal
                {...this.props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Sauvegarder cet aliment
                    </Modal.Title>

                </Modal.Header>
                <Modal.Body>
                    <hr/>
                    <Form>
                        <Form.Group className="mb-3 infoFoodTitle" controlId="exampleForm.ControlInput1">
                            <Form.Label>Nom de l'aliment</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="riz blanc cuit"
                                onChange={this.handleFoodNameChange}
                                autoFocus
                                required
                            />
                        </Form.Group>
                        <div className={"infoFoodContainer"}>
                            <Form.Group className="mb-3 infoFoodTitle" controlId="exampleForm.ControlInput1">
                                <Form.Label>Quantité Référence</Form.Label>
                                <Form.Control
                                    type="text"
                                    value={this.state.quantity}
                                    onChange={this.handleQuantityChange}
                                    required
                                />
                            </Form.Group>
                            <Form.Group className="mb-3 infoFoodTitle" controlId="exampleForm.ControlInput1">
                                <Form.Label>Calories Références</Form.Label>
                                <Form.Control
                                    type="text"
                                    value={this.state.calories}
                                    onChange={this.handleCaloriesChange}
                                    required
                                />
                            </Form.Group>

                        </div>
                    </Form>
                    <hr/>
                </Modal.Body>
                <Modal.Footer>
                    <Button className={"saveButton"} onClick={this.onSaveFood}>Enregistrer</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}

export default SaveFoodRefModal;
