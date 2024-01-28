import { Camera, CameraType } from 'expo-camera';
import { useRef, useState } from 'react';
import { StyleSheet, TouchableOpacity, View, Image } from 'react-native';
import { Button, ActivityIndicator, Modal, Portal, Text, PaperProvider } from 'react-native-paper';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import { sendImage } from '../../utils';

export default function CameraComponent({ navigation }) {
    const cameraRef = useRef(null);
    const [type, setType] = useState(CameraType.back);
    const [clicked, setClicked] = useState(false);
    const [image, setImage] = useState(null);
    const [prediction, setPrediction] = useState(null);
    // const [labeledPrediction, setLabeledPrediction] = useState(null);
    const [modalImage, setModalImage] = useState(null); 
    const [transparent, setTransparent] = useState(null);
    const [loading, setLoading] = useState(false);
    const [permission, requestPermission] = Camera.useCameraPermissions();
    const [visible, setVisible] = useState(false);

    const showModal = () => setVisible(true);
    const hideModal = () => setVisible(false);
    const containerStyle = { padding: 20, zIndex: 10000};

    if (!permission) {
        // Camera permissions are still loading
        return <View />;
    }

    if (!permission.granted) {
        // Camera permissions are not granted yet
        return (
            <>
                <Text style={{ textAlign: 'center' }}>We need your permission to show the camera</Text>
                <Button mode="contained" onPress={requestPermission} title="Grant permission" />
            </>
        );
    }

    const toggleCameraType = () => {
        setType(current => (current === CameraType.back ? CameraType.front : CameraType.back));
    }

    const takePicture = async () => {
        if (cameraRef.current) {
            setLoading(true);
            const data = await cameraRef.current.takePictureAsync({ base64: true });
            setClicked(true);
            setImage(data.uri);
            const response = await sendImage(data.uri);
            // console.log(response);
            setLoading(false);
            setImage("data:image/jpeg;base64," + response.labeled);
            setPrediction("data:image/jpeg;base64," + response.prediction);
            // setLabeledPrediction("data:image/jpeg;base64," + response.labeled_prediction);
            setTransparent("data:image/png;base64," + response.transparent);
            setModalImage("data:image/jpeg;base64," + response.prediction);
            //navigation.navigate('Home', { base64: data.base64, uri: data.uri });
        }
    }

    return (
        <View style={styles.container}>
            <Camera ref={cameraRef} style={styles.camera} type={type}>
                    {clicked && <>
                        <Image source={{ uri: prediction }} style={{ position: 'absolute', top: 0, left: 0, bottom: 0, right: 0, opacity: 0.3, justifyContent: "center", alignItems: "center", width: "100%", height: "100%", zIndex: 999 }} />
                        <Image source={{ uri: transparent }} style={{ position: 'absolute', top: 0, left: 0, bottom: 0, right: 0, justifyContent: "center", alignItems: "center", width: "100%", height: "100%", zIndex: 999 }} />
                    </>}
                    {!visible && <>
                        <TouchableOpacity style={{alignSelf: "flex-start", zIndex: 999}} onPress={toggleCameraType}>
                        <MaterialCommunityIcons name="camera-flip" color={"#fff"} size={40} />
                    </TouchableOpacity>
                    <View style={styles.buttonContainer}>
                        <TouchableOpacity style={styles.button} onPress={takePicture}>
                            <MaterialCommunityIcons name="circle-slice-8" color={"#fff"} size={80} />
                        </TouchableOpacity>
                        </View>

                        </>}
                    {clicked && <>
                    <View style={{ position: "absolute", top: 0, left: 0, right: 0, bottom: 0, flex: 1, padding: 5, alignItems: "flex-end", justifyContent: "center", zIndex: 999 }}>
                        <TouchableOpacity style={styles.button} onPress={() => { setClicked(false); setImage(null); setPrediction(null); setVisible(false) }}>
                            <MaterialCommunityIcons name="close-circle" color={"#fff"} size={40} />
                        </TouchableOpacity>
                        <View style={{ flex: 1, width: "100%", marginTop: 10 }}>
                            <PaperProvider>
                                <Portal>
                                    <Modal visible={visible} onDismiss={hideModal} contentContainerStyle={containerStyle}>
                                        <Image source={{ uri: modalImage }} style={{ width: "100%", height: "90%", marginBottom: 3 }} />
                                        <View style={{ flexDirection: "row", justifyContent: "space-evenly" }}>
                                        <Button mode="contained" onPress={() => {setModalImage(prediction)}}>Cool pose</Button>
                                        <Button mode="contained" onPress={() => {setModalImage(image)}}>Your pic</Button>
                                        </View>
                                    </Modal>
                                </Portal>
                                <TouchableOpacity style={styles.button} onPress={showModal}>
                                    <Image source={{ uri: prediction }} style={{ height: 60, width: 60, borderColor: "white", borderWidth: 1, ...styles.imageShadow }} />
                                </TouchableOpacity>
                            </PaperProvider>
                        </View>
                    </View>
                </>}

                    {loading &&
                    <View style={styles.loading}>
                        <Text style={{ fontSize: 20, fontWeight: "bold", color: "#663399", alignSelf: "center", zIndex: 999 }}>Coming up with some cool poses...</Text>
                        <ActivityIndicator size='large' style={{zIndex: 9999}} />
                        <Image source={{ uri: image }} style={{ position: 'absolute', top: 0, left: 0, bottom: 0, right: 0, justifyContent: "center", alignItems: "center", width: "100%", height: "100%" }} />
                    </View>
                }
    
                {/* {clicked && <>
                    <View style={{ position: "absolute", top: 0, left: 0, right: 0, bottom: 0, flex: 1, padding: 5, alignItems: "flex-end", justifyContent: "center", zIndex: 999 }}>
                        <TouchableOpacity style={styles.button} onPress={() => { setClicked(false); setImage(null); setPrediction(null); }}>
                            <MaterialCommunityIcons name="close-circle" color={"#fff"} size={40} />
                        </TouchableOpacity>
                        <View style={{ flex: 1, width: "100%", marginTop: 10 }}>
                            <PaperProvider>
                                <Portal>
                                    <Modal visible={visible} onDismiss={hideModal} contentContainerStyle={containerStyle}>
                                        <Image source={{ uri: prediction }} style={{ width: "100%", height: "90%", marginBottom: 3 }} />
                                        <Button mode="contained" onPress={() => {setPrediction(labeledPrediction)}}>See landmarks</Button>
                                    </Modal>
                                </Portal>
                                <TouchableOpacity style={styles.button} onPress={showModal}>
                                    <Image source={{ uri: prediction }} style={{ height: 60, width: 60, borderColor: "white", borderWidth: 1, ...styles.imageShadow }} />
                                </TouchableOpacity>
                            </PaperProvider>
                        </View>
                    </View>
                    <Image source={{ uri: image }} style={{ flex: 1 }} />
                </>} */}
            </Camera>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
    },
    camera: {
        flex: 1,
    },
    buttonContainer: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: "center",
        backgroundColor: 'transparent',
        margin: 64,
        zIndex: 1000
    },
    button: {
        alignSelf: 'flex-end',
        zIndex: 10000
    },
    text: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
    },
    loading: {
        flex: 1,
        position: 'absolute',
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
        alignItems: 'center',
        justifyContent: 'center'
    },
    imageShadow: {
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 5,
        },
        shadowOpacity: 0.36,
        shadowRadius: 6.68,
    }
});