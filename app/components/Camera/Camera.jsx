import { Camera, CameraType } from 'expo-camera';
import { useRef, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View, Image } from 'react-native';
import { Button, ActivityIndicator } from 'react-native-paper';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import { sendImage } from '../../utils';

export default function CameraComponent({ navigation }) {
    const cameraRef = useRef(null);
    const [type, setType] = useState(CameraType.back);
    const [clicked, setClicked] = useState(false);
    const [image, setImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [permission, requestPermission] = Camera.useCameraPermissions();

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
            console.log(response);
            setLoading(false);
            setImage("data:image/jpeg;base64," + response.base64);
            //navigation.navigate('Home', { base64: data.base64, uri: data.uri });
        }
    }

    return (
        <View style={styles.container}>
            <Camera ref={cameraRef} style={styles.camera} type={type}>
                {!clicked && <>
                    <TouchableOpacity style={styles.button} onPress={toggleCameraType}>
                        <MaterialCommunityIcons name="camera-flip" color={"#fff"} size={40} />
                    </TouchableOpacity>
                    <View style={styles.buttonContainer}>
                        <TouchableOpacity style={styles.button} onPress={takePicture}>
                            <MaterialCommunityIcons name="circle-slice-8" color={"#fff"} size={80} />
                        </TouchableOpacity>
                    </View>
                </>}
                {clicked && <>
                    <Button mode="contained" onPress={() => { setClicked(false); setImage(null); }}>X</Button>
                    <Image source={{ uri: image }} style={{ flex: 1 }} />
                </>}
                {loading &&
                    <View style={styles.loading}>
                        <Text style={{ fontSize: 20, fontWeight: "bold", color: "#663399", alignSelf: "center" }}>Coming up with some cool poses...</Text>
                        <ActivityIndicator size='large' />
                    </View>
                }
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
    },
    button: {
        alignSelf: 'flex-end',
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
    }
});