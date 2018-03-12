function [ scaleSpace ] = generateScaleSpace( img_GrayScale, scales, sigma, k, n)

    [h,w] = size(img_GrayScale);
    scaleSpace = zeros(h, w, scales); 
    gaussain= zeros(h, w, scales+1);
    switch n 
        case 1
            j=1;
            while j<=scales+1
                   %filteredImage=gaussian_filter(img_GrayScale,sigma,k,j);
                  scaledSigma = sigma * k^(j-1);
                    kernelSize = max(1,fix(6*scaledSigma)+1);
                    filteredImage=imgaussfilt(img_GrayScale,scaledSigma);
                   gaussian(:,:,j)=filteredImage;
                   j=j+1;
            end
            %disp("1");
            i=1;
            while i<=scales
                scaleSpace(:,:,i)=gaussian(:,:,i+1)-gaussian(:,:,i);
                i=i+1;
                %disp("2");
            end
        case 2
            j = 1;
            while j <= scales
                
                LoGKernel = createFilter(j, sigma, k); 
                filteredImage = imfilter(img_GrayScale, LoGKernel,'same', 'replicate'); 
                filteredImage = filteredImage .^ 2;

                scaleSpace(:,:,j) = filteredImage;   
                j = j + 1;
            end
    end
    
   

end
function [LogKernel] = createFilter(j, sigma, scaleMultiplier)
    scaledSigma = sigma * scaleMultiplier^(j-1);
    kernelSize = max(1,fix(6*scaledSigma)+1);  
    % Create a Laplacian of Gaussian kernel ('log')
    LogKernel = fspecial( 'log', kernelSize, scaledSigma );
    % Normalize the kernel 
    LogKernel = scaledSigma.^2 * LogKernel;
end
