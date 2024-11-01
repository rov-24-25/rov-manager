use tokio::net::TcpListener;
use tokio::io::AsyncReadExt;
use serde::{Serialize, Deserialize};
use serialport;
use serde_json;
use std::time::Duration;

#[derive(Serialize, Deserialize,Debug)]
struct DataPackage {
    motors: Vec<f32>,
}




#[tokio::main]
async fn main() -> Result<(),Box<dyn std::error::Error>> {
        let listener = TcpListener::bind("169.254.85.12:12345").await?;

        
        let (mut socket, _) = listener.accept().await?;

            tokio::spawn(async move {
                let port_name = "/dev/ttyUSB0"; // Adjust this according to your system
                let baud_rate = 9600;
                let mut port = serialport::new(port_name,baud_rate)
                .timeout(Duration::from_millis(10)).open().expect("failed to open port");
            let mut buf = [0u8; 4];
            //let mut buf = vec![0; 1024];
            loop{
                let mut data_points = Vec::new();
                for _ in 1..5{
                match socket.read_exact(&mut buf).await{

                Ok(_) => {
                    let data_point = f32::from_le_bytes(buf);
                    data_points.push(data_point);
                    println!("Received data point: {}", data_point);
                    
                },
                Err(e) => {
                    println!("Failed to read from socket; err = {:?}", e);
                    return;
                }
            }
            }

            let mut motors=Vec::new();
            let theta=data_points[2].atan2(data_points[1]);
            let norm=(data_points[1].powi(2)+data_points[2].powi(2)).sqrt();
            let cons=(1.0-theta.sin())/(theta.cos()+1e-6);
            //on met une constante pour éviter les problèmes quand cos(theta)=0
            let left=(1.0+cons)*0.5*norm*255.0;
            let right=1.0-cons*0.5*norm*255.0;
            motors.push(left);
            motors.push(right);
            motors.push(0.0);
            //soit O l'angle entre x et la direction pointée, la puissance des moteurs sera 0.5(+-)0.5*cos(O)
            motors.push(((data_points[0]+1.0)/2.0)*255.0);


            let package=DataPackage{motors};
            let serialized = serde_json::to_vec(&package);
            //port.write(serialized);
            
            match serialized {
                Ok(vec) => {
      //          let slice: &[u8]=&vec; 
                let _= port.write(&vec);
                println!("motors: {:#?}",package);
                },
                Err(e) => {
                    eprintln!("Serialization error: {:?}", e);
                }
            }
            
        }
            
        });
        Ok(())
    }
   


