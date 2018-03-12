function [ scaleSpace3D ] = detectBlobs( img_GrayScale, scales, sigma, k, threshold, n )

[h, w] = size(img_GrayScale); 

display('Generating Scale Space'); tic;
scaleSpace = generateScaleSpace(img_GrayScale, scales, sigma, k, n);
display('Finished generating scale space'); toc;

scaleSpace2D = zeros(h,w,scales);
i = 1;
while i <= scales
    scaleSpace2D(:,:,i) = nms_2D(scaleSpace(:,:,i),1);
    i = i + 1;
end

scaleSpace3D = nms_3D(scaleSpace2D, scaleSpace, scales);

threshBinaryFlag = scaleSpace3D > threshold;

scaleSpace3D = scaleSpace3D .* threshBinaryFlag;

end

function [ img2DNMS ] = nms_2D(img, radius)

    neighborhood = 2*radius+1; %size of mask
    domain = ones(3,3);

    img2DNMS = ordfilt2(img, neighborhood^2, domain);
    
end

function [ scaleSpace3D ] = nms_3D( scaleSpace2D, originalScaleSpace, scales ) 
i = 1;
while i <= scales
    if i == 1
        lowerScale = i;
        upperScale = i+1;
    elseif i < scales
        lowerScale = i-1;
        upperScale = i+1;
    else
        lowerScale = i-1;
        upperScale = i;
    end
    scaleSpace2D(:,:,i) = max(scaleSpace2D(:,:,lowerScale:upperScale),[],3);
    i = i+1;
end

originalMarkers = scaleSpace2D == originalScaleSpace;
scaleSpace3D = scaleSpace2D .* originalMarkers;

end
