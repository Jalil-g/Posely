import { Camera, CameraType } from 'expo-camera';
import { useRef, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Button } from 'react-native-paper';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import { sendImage } from '../../utils';

export default function CameraComponent({ navigation }) {
    const cameraRef = useRef(null);
    const [type, setType] = useState(CameraType.back);
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
            const data = await cameraRef.current.takePictureAsync({ base64: true });
            await sendImage(data.base64);
            navigation.navigate('Home', { base64: data.base64, uri: data.uri });
        }
    }

    return (
        <View style={styles.container}>
            <Camera ref={cameraRef} style={styles.camera} type={type}>
                <TouchableOpacity style={styles.button} onPress={toggleCameraType}>
                    <MaterialCommunityIcons name="camera-flip" color={"#fff"} size={40} />
                </TouchableOpacity>
                <View style={styles.buttonContainer}>
                    <TouchableOpacity style={styles.button} onPress={takePicture}>
                        <MaterialCommunityIcons name="circle-slice-8" color={"#fff"} size={80} />
                    </TouchableOpacity>
                </View>
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
});